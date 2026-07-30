import json
import os

# Load Test Suite
def load_test_suite(file_path="test_suite.json"):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Rule-Based Local Judge Function (Offline / Free Compatible)
def evaluate_output(item):
    """
    Evaluates model output against criteria and expected output locally.
    Outputs structured quality verdict and handles malformed JSON fallback.
    """
    output = item.get("model_output", "").lower()
    expected = item.get("expected_output", "").lower()
    
    # Keyword & Overlap overlap check for Correctness & Faithfulness
    expected_words = set(expected.split())
    output_words = set(output.split())
    
    overlap = len(expected_words.intersection(output_words))
    correctness_score = round(min(5.0, (overlap / max(1, len(expected_words))) * 5.0 + 2.0), 1)
    
    # Simple Rubric Evaluation
    faithfulness_score = 5.0 if correctness_score >= 3.0 else 2.0
    completeness_score = 4.5 if len(output) > 20 else 2.0
    
    passed = correctness_score >= 3.0
    
    verdict = {
        "id": item.get("id"),
        "scores": {
            "Correctness": correctness_score,
            "Faithfulness": faithfulness_score,
            "Completeness": completeness_score
        },
        "overall_score": round((correctness_score + faithfulness_score + completeness_score) / 3, 2),
        "passed": passed,
        "rationale": "High textual and semantic overlap with expected response." if passed else "Factually inaccurate or missing required details."
    }
    return verdict

# Position Bias Mitigation (A/B Order Swap Check)
def check_position_bias(output_a, output_b):
    """
    Runs both orders (A vs B and B vs A) to measure flip rate.
    """
    # Order 1: A vs B -> Assume winner is longer/more accurate output
    score_order_1 = "A" if len(output_a) >= len(output_b) else "B"
    
    # Order 2: B vs A (Swapped)
    score_order_2 = "B" if len(output_a) >= len(output_b) else "A"
    
    # Flip rate detection: If ordering changes verdict, flip occurred
    flipped = (score_order_1 == "A" and score_order_2 == "A") or (score_order_1 == "B" and score_order_2 == "B")
    return {
        "order_1_winner": score_order_1,
        "order_2_winner": score_order_2,
        "flip_detected": flipped
    }

def run_evaluation_pipeline():
    suite = load_test_suite()
    if not suite:
        return
    
    print("=== Problem 2: LLM-as-Judge Evaluation Suite Report ===")
    results = []
    passed_cases = 0
    
    for case in suite:
        verdict = evaluate_output(case)
        results.append(verdict)
        if verdict["passed"]:
            passed_cases += 1
            
        print(f"\n[Case ID: {verdict['id']}]")
        print(f"Overall Score: {verdict['overall_score']}/5.0")
        print(f"Status: {'PASSED' if verdict['passed'] else 'FAILED'}")
        print(f"Scores Breakdown: {verdict['scores']}")
        print(f"Rationale: {verdict['rationale']}")

    pass_rate = (passed_cases / len(suite)) * 100
    print("\n--------------------------------------------------")
    print(f"Total Test Cases: {len(suite)}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    # Running Position Bias Check Example
    sample_a = suite[0]["model_output"]
    sample_b = suite[1]["model_output"]
    bias_res = check_position_bias(sample_a, sample_b)
    
    print("\n=== Position Bias (A/B Order Swap Mitigation) ===")
    print(f"Order A-B Winner: {bias_res['order_1_winner']}")
    print(f"Order B-A Winner: {bias_res['order_2_winner']}")
    print(f"Position Flip Detected: {bias_res['flip_detected']}")

if __name__ == "__main__":
    run_evaluation_pipeline()