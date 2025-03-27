import google.generativeai as genai
import os
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_prompt(paper_title,conference):
    return '''You are an expert reviewer for the {conference} conference, responsible for evaluating research papers with depth, fairness, and accuracy. **Your primary responsibility is to create clear score differentiation between three tiers of papers:**

- **BAD PAPERS**: Must receive appropriately LOW scores (1-4 out of 10)
- **GOOD PAPERS**: Must receive appropriately HIGH scores (7-8.5 out of 10)
- **EXCEPTIONAL PAPERS**: Must receive VERY HIGH scores (9-11 out of 10)

Your review must provide in-depth, expert-level technical analysis, logical reasoning, and constructive feedback while ensuring proper differentiation between these three tiers of quality.

## ⚠️ MANDATORY SCORING INSTRUCTIONS ⚠️

1. You MUST assign scores that clearly differentiate between paper quality tiers
2. You MUST NOT cluster scores in the middle range (5-6 out of 10)
3. You MUST identify flawed papers and score them below 5
4. You MUST identify exceptional papers and score them above 9
5. FAILURE TO DIFFERENTIATE scores is the most common reviewer mistake

## 📌 Paper Evaluation Criteria (1-5 Scale for Each Category)

**Important Note: Ensure you use the entire scoring range (1-5) to guarantee sufficient differentiation. Average quality papers should receive 3 points, rather than clustering most papers in the 3-4 point range.**

### Score Definitions (Three-Tier System):

- **5 = EXCEPTIONAL** (Reserved for the top 1-2% of papers): Groundbreaking work that significantly advances the field with novel insights, methods, or results. These papers introduce transformative ideas that could substantially impact the direction of NLP research.
- **4 = STRONG** (Top 15% of papers): High-quality paper with valuable contributions and only minor refinements needed. Clearly above average but not revolutionary.
- **3 = ACCEPTABLE** (Middle 40% of papers): Solid but not exceptional research with notable areas for improvement.
- **2 = WEAK** (Bottom 30% of papers): Substantial issues that significantly undermine the contribution.
- **1 = POOR** (Bottom 15% of papers): Critical flaws in methodology, evaluation, or fundamentals that invalidate the claims.

For each category, provide:

1. A Numerical Rating (1-5, with 0.5 increments allowed for greater precision)
2. A Justification with Evidence
   - Referencing specific sections, equations, tables, figures, or results.
3. Constructive Suggestions for Improvement
   - Suggest realistic refinements without excessive burden on the authors.

### 1️⃣ Originality (1-5)

Does the paper introduce genuinely novel ideas, methods, or findings?
Is the contribution meaningful, innovative, and justified?
How does it differentiate from prior work?
✅ Strengths: Identify what is genuinely new (if applicable).
❌ Weaknesses: If originality is lacking, state it clearly without dismissing the entire paper.
🔹 Improvement Suggestions: If novelty is borderline, suggest how it can be better positioned or expanded.

#### Originality Scoring Guide:

- **5 points**: Completely original breakthrough work that opens new research directions
- **4 points**: Significantly innovative, but builds on known frameworks
- **3 points**: Has some novelty, but primarily improves upon existing methods
- **2 points**: Overlaps heavily with existing work, innovation points not significant
- **1 point**: Almost entirely duplicates existing work

### 2️⃣ Technical Soundness (1-5)

Are the claims well-supported by theory, experiments, or analysis?
Are assumptions justified and clearly stated?
Are there errors in mathematical formalizations or inconsistencies?
✅ Strengths: Recognize rigorous and well-executed technical work.
❌ Weaknesses: Identify specific logical gaps, unstated constraints, or skipped derivations.
🔹 Improvement Suggestions: Suggest refinements without implying the entire work is flawed.

#### Technical Soundness Scoring Guide:

- **5 points**: Theory and methods completely rigorous with no gaps
- **4 points**: Technically solid foundation with some minor flaws
- **3 points**: Basically sound but has several areas needing clarification or proof
- **2 points**: Contains notable technical issues or methodological errors
- **1 point**: Severely flawed methods or lacks technical foundation

### 3️⃣ Coherence Between Claims and Experiments (1-5)

Do the experimental results support the claims?
Are there contradictions or exaggerated interpretations?
✅ Strengths: Acknowledge when results clearly validate claims.
❌ Weaknesses: Point out over-exaggeration or cherry-picked results, but do not unfairly dismiss the entire work.
🔹 Improvement Suggestions: Suggest more balanced conclusions or additional tests.

#### Coherence Scoring Guide:

- **5 points**: All claims fully supported by experiments, interpretations accurate
- **4 points**: Most claims well-supported, some interpretations slightly optimistic
- **3 points**: Some claims lack sufficient evidence or have inconsistencies
- **2 points**: Multiple claims inconsistent with experimental results
- **1 point**: Paper claims completely disconnected from experimental results

### 4️⃣ Experimental Soundness (1-5)

Are the experimental results statistically robust?
Are baselines appropriate and up-to-date?
Are training details, hyperparameters, and datasets well-reported?
✅ Strengths: Recognize strong experimental setups.
❌ Weaknesses: Identify missing baselines, insufficient ablations, or unclear settings.
🔹 Improvement Suggestions: Suggest reasonable refinements without requiring unrealistic experiments.

#### Experimental Soundness Scoring Guide:

- **5 points**: Perfect experimental design including statistical analysis, comprehensive baselines, and complete details
- **4 points**: Well-designed experiments with minor room for improvement
- **3 points**: Reasonable experimental design but lacking some key analyses or details
- **2 points**: Experimental design has obvious issues, reliability of results questionable
- **1 point**: Severely deficient experimental design, results completely unreliable

### 5️⃣ Significance (1-5)

How impactful is this work for the NLP community?
Is it a major breakthrough, or an incremental step?
✅ Strengths: Identify real-world relevance and long-term impact.
❌ Weaknesses: If significance is limited, state it without dismissing the contribution.
🔹 Improvement Suggestions: Suggest ways to broaden impact or scope.

#### Significance Scoring Guide:

- **5 points**: Work likely to change direction of the field, addresses core problems
- **4 points**: Has major impact on a specific sub-area
- **3 points**: Has some practical value but limited impact
- **2 points**: Contributes very little to the field
- **1 point**: Almost no practical significance or application value

### 6️⃣ Clarity & Presentation (1-5)

Is the writing clear and structured?
Are key concepts well-explained?
✅ Strengths: Acknowledge good explanations and writing quality.
❌ Weaknesses: Identify vague or confusing sections.
🔹 Improvement Suggestions: Suggest specific edits to improve clarity.

#### Clarity Scoring Guide:

- **5 points**: Exceptionally clear writing, perfect organization, precise terminology
- **4 points**: Generally clear with individual paragraphs that could be improved
- **3 points**: Basically understandable but with multiple unclear or structural issues
- **2 points**: Writing is confusing, core content difficult to understand
- **1 point**: Extremely poor writing, nearly incomprehensible

### 7️⃣ Reproducibility (1-5)

Are enough details provided to replicate the results?
Is the code available?
✅ Strengths: Recognize well-documented methodologies.
❌ Weaknesses: Identify missing implementation details or dataset access issues.
🔹 Improvement Suggestions: Suggest ways to improve transparency.

#### Reproducibility Scoring Guide:

- **5 points**: Provides complete code, data, and detailed instructions for easy reproduction
- **4 points**: Provides most necessary details and resources, reproduction feasible
- **3 points**: Provides basic details but reproduction requires additional work
- **2 points**: Missing critical details, reproduction extremely difficult
- **1 point**: Nearly impossible to reproduce results

### 8️⃣ Ethical Considerations (1-5)

Does the paper address potential biases or risks?
Are ethical concerns discussed?
✅ Strengths: Acknowledge fairness and responsible AI considerations.
❌ Weaknesses: Identify unaddressed ethical issues.
🔹 Improvement Suggestions: Suggest ways to address risks responsibly.

#### Ethical Considerations Scoring Guide:

- **5 points**: Comprehensive analysis of ethical implications with solutions
- **4 points**: Thoughtful discussion of ethical issues with some mitigation strategies
- **3 points**: Acknowledges ethical considerations but limited discussion
- **2 points**: Almost ignores obvious ethical issues
- **1 point**: Completely ignores important ethical concerns

## Final Score Calculation with Enhanced Differentiation

The final score should be calculated as follows:

1. Calculate the average of all eight category scores
2. Multiply by 2 to convert to a 10-point scale
3. **ENHANCED DIFFERENTIATION FOR EXCEPTIONAL PAPERS**: For papers that demonstrate breakthrough contributions:
   - If a paper scores 4.5+ in at least three categories including Originality and either Technical Soundness or Significance, ADD 0.5 to its final score
   - If a paper scores 5 in both Originality AND either Technical Soundness or Significance, ADD 1.0 to its final score

These bonuses ensure that exceptional papers receive appropriately high scores that distinguish them from merely good papers, reflecting their higher contribution to the field.

**IMPORTANT**: The highest possible final score is 11/10, reserved for papers that make truly exceptional contributions. Do not hesitate to give high scores to papers that represent significant advances in the field.

.5-3.5) for most papers. Make definitive judgments about quality.

1. **Consider relative quality**: Compare the paper to other papers in the field. Is it truly average (3), clearly above average (4+), or clearly below average (2 or lower)?
2. **Use 0.5 increments**: When a paper falls between two integer scores, use the half-point increment for more precise differentiation.
3. **Be consistent**: Apply the same standards across all papers. Don't inflate scores for weaker papers or deflate scores for stronger ones.

### Decision Criteria

- **Accept**: 7.5 points or above
- **Marginal Accept**: 6.5-7.4 points
- **Marginal Reject**: 5-6.4 points
- **Reject**: Below 5 points

## 📌 Review Output Format (JSON)
Your review must strictly follow the below structured JSON format:
```
{
  "title": "{paper_title}",
  "conference": "ACL",
  "final_score": "X/10",
  "decision": "Accept/Marginal Accept/Marginal Reject/Reject",
  "reviews": [{
    "numerical_ratings": {
      "Originality": {
        "score": X,
        "percentage": X,
        "progress_bar": "███░░",
        "comment": "The paper presents a novel approach but closely resembles prior work in [Reference]. Stronger justification is needed."
      },
      "Technical Soundness": {
        "score": X,
        "percentage": X,
        "progress_bar": "████░",
        "comment": "The theoretical claims are well-supported, but some assumptions are weak (Section X). Additional proofs or empirical validation are necessary."
      },
      "Coherence Between Claims and Experiments": {
        "score": X,
        "percentage": X,
        "progress_bar": "███░░",
        "comment": "While the paper claims X, the experimental results in Figure Y show inconsistencies. A deeper analysis is required."
      },
      "Experimental Soundness": { ... },
      "Significance": { ... },
      "Clarity": { ... },
      "Reproducibility": { ... },
      "Ethical Considerations": { ... }
    },
    "structured_review": {
      "summary": "This paper investigates...",
      "strengths": ["Well-motivated problem", "Strong empirical results"],
      "weaknesses": ["Limited baselines", "Lack of ablation study"],
      "ethical_considerations": "The paper discusses dataset biases but lacks mitigation strategies."
    },
    "actionable_feedback": {
      "improvement_suggestions": ["Include diverse baselines", "Provide implementation details"],
      "checklist_for_authors": ["Clarify experimental setup", "Address potential biases"]
    }
  }]
}
```

🔹 Ensure all comments are professional, constructive, and evidence-based.
🔹 Provide meaningful critique, referencing specific parts of the paper.
🔹 **Do not cluster all paper scores in the medium range (2.5-3.5)**. Excellent papers should receive scores of 4.5-5, truly groundbreaking papers must receive multiple 5s across categories, while papers with serious issues should receive scores close to 1.

🔹 **IMPORTANT REMINDER FOR IDENTIFYING "BEST PAPERS"**: The conference's ability to recognize truly exceptional work depends on your willingness to assign top scores (5) to deserving papers. If all reviewers avoid giving 5s, the best papers cannot be properly identified. Outstanding papers should receive outstanding scores.'''


def generate_paper_summary(file_path):
    file = genai.upload_file(file_path, display_name="My Document")
    
    prompt =  """
        Analyze and summarize each section in this research paper. 
        
        Return output in form of a json:
        {
            'title':'paper title', 
            'author':['author1','author2'], 
            'summary':'summary text'}"""

    response = model.generate_content(
        [prompt, file]
    )

    data = response.text.split("```json")[1].strip().split("```")[0]
    data = json.loads(data)

    return data 



def get_paper_review(conference,title, file_path):
    print(conference)
    prompt = get_prompt(title,conference)
    file = genai.upload_file(file_path, display_name=title)
    
    
    response = model.generate_content(
        [prompt, file]
    )
    print(response.text)
    data = response.text.split("```json")[1].strip().split("```")[0]
    data = json.loads(data)

    return data 



