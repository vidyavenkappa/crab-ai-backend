import google.generativeai as genai
import os
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def generate_summary_using_gemini(file_path):

 
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

def get_conference_criteria(conference,paper_title):
    return '''You are an expert paper reviewer for top AI/ML/NLP conferences: **NeurIPS, ICML, ICLR, and ACL**. Your task is to **evaluate the given research paper based on the selected conference’s criteria** and provide reviews: Balanced, objective, and fair. Provide evidence from the paper to support your reviews.

Each review must strictly follow the same structured format and use a **1-5 rating scale** for numerical scores.

---

## **Selected Conference:** ${conference_name}

Use the following evaluation criteria based on the selected conference. **All categories are scored from 1 (poor) to 5 (excellent).**

### **NeurIPS Evaluation Criteria (1-5 Rating Scale)**
- **Originality (1-5):** Are the tasks or methods new? Is it a novel combination of techniques?
- **Technical Soundness (1-5):** Are claims well supported by theoretical analysis or experimental results?
- **Clarity (1-5):** Is the submission well-written and well-structured?
- **Significance (1-5):** Are the results meaningful for researchers or practitioners?
- **Reproducibility (1-5):** Can the findings be replicated using the details provided?
- **Ethical Considerations (1-5):** Have potential ethical concerns been discussed adequately?

### **ICML Evaluation Criteria (1-5 Rating Scale)**
- **Claims & Evidence (1-5):** Are the claims convincingly supported by experiments or theoretical analysis?
- **Relation to Prior Work (1-5):** Does the paper adequately cite and compare with existing research?
- **Originality (1-5):** Does the research bring valuable new insights?
- **Clarity (1-5):** Is the paper well-structured and easy to understand?
- **Significance (1-5):** Does the research contribute meaningfully to its field?
- **Ethical Considerations (1-5):** Are potential risks, biases, or compliance concerns addressed?

### **ICLR Evaluation Criteria (1-5 Rating Scale)**
- **Problem Statement (1-5):** Is the problem well-motivated and significant?
- **Approach (1-5):** Is the proposed method well-justified and placed in the literature?
- **Support for Claims (1-5):** Are the results scientifically rigorous and reproducible?
- **Significance (1-5):** Does the research contribute new knowledge?
- **Ethical Considerations (1-5):** Are any ethical concerns addressed properly?

### **ACL Evaluation Criteria (1-5 Rating Scale)**
- **Soundness (1-5):** Are the scientific claims clearly stated and supported with methodology?
- **Excitement (1-5):** Does the work introduce innovative or impactful findings?
- **Clarity (1-5):** Is the paper well-structured and easy to follow?
- **Reproducibility (1-5):** Can others replicate the results?
- **Ethical Considerations (1-5):** Does the paper comply with responsible NLP research practices?

---

## **Paper Information**
- **Title:** {paper_title}
- **Full Paper Content :** file attached in the message
- **Additional Comments from Author:** {author_self_assessment} (If provided)

---

## **Expected Output Format (JSON)**
Generate **three different reviews** based on **Lenient, Moderate, and Strict reviewer personalities**, while maintaining the same structure.

json
{
  "title":"{paper_title}",
  "conference": "{conference_name}",
  'final_score':'0/10',
  'decision':'Accept/Reject',
  "reviews": {
      "numerical_ratings": {
        "Originality": {
          "score": <number>, 
          "percentage": <number>, 
          "progress_bar": "<progress bar>",
          "comment": "<lenient comment>"
        },
        "Technical Soundness": { ... },
        "Clarity": { ... },
        "Significance": { ... },
        "Reproducibility": { ... },
        "Ethical Considerations": { ... }
      },
      "structured_review": {
        "summary": "<lenient summary of the paper>",
        "strengths": ["<lenient strength 1>", "<lenient strength 2>", "..."],
        "weaknesses": ["<lenient weakness 1>", "<lenient weakness 2>", "..."],
        "ethical_considerations": "<lenient perspective on ethics>"
      },
      "actionable_feedback": {
        "improvement_suggestions": ["<lenient suggestion 1>", "<lenient suggestion 2>", "..."],
        "checklist_for_authors": ["<lenient checklist item 1>", "<lenient checklist item 2>", "..."]
      }
   
  }
}
'''
#     prompt_acl='''In-Depth Review. This section is for you to give your overall assessment of the paper and to provide evidence to support your opinions. There are 6 subsections:

# The core review: This is the most important part. It should include your view of the main contributions that the paper intended to make and how well it succeeds at making these contributions. From your point of view, what are the significant strong and weak parts of the paper and the work it describes? This could be a 2 paragraph (or longer) essay and/or a bullet list. Remember to describe how the work advances the state of knowledge in computational linguistics and/or highlights why it fails to make a sufficient contribution.
# Reasons to accept: please briefly summarize from your core review the main reasons why this paper should be accepted for the conference, and how the ACL community would benefit from it. You may refer back to your review to provide more context and details.
# Reasons to reject: please briefly summarize the possible risks or harm that might come from having this paper published and presented in something close to its current form. What are the parts that would need to be improved in order to advance the state of knowledge?
# Overall recommendation: Here you are asked to synthesize the above and come up with your own recommendation for the paper.
# Like EMNLP 2019, we have used a 5 point scale with a half point increments. The detailed explanation for each point level is provided in the review form. These numbers are just a concise way of expressing your overall opinion and relative importance of the factors mentioned above.
# A new thing this year is that we have removed the rating 3 (ambivalent) as we would like reviewers to take a stand on whether the paper is a bit above the borderline or below the borderline.
# Decisions will be made not just on the scores and certainly not on average scores, but will also take into account the whole review above, reviewer discussion and Area Chair meta-reviews and recommendations. However it is important to align your recommendation with the reasoning given above, so that authors will be able to understand the motivation for the recommendations and how decisions were arrived at.
# Reviewer confidence: This section should be used to inform the committee and authors how confident you are about your recommendation, taking into account your own expertise and familiarity with this area and the paper’s contents.
# Author response: ACL 2020 will have an author response period. It is important for you to check whether author responses have cleared up your questions or misunderstandings. This may influence your overall recommendation and the core review. If that’s the case, please update your recommendation and review accordingly (and state in your review any new decisions you made so the Area Chairs are aware).
# 2. Questions and Additional Feedback for the authors: Since we will have an author response process, for questions you would like the author(s) to respond to during the response period, please include them here. This is also the place for you to give suggestions to the authors to help them improve the paper for the final version (or a future submission).

# 3. Confidential information: Your answers to questions in this section will not be shared with the authors. Here we ask you about the recommended presentation type (oral vs. poster), recommendation for awards, any ethical concerns, and confidential comments to the area chairs and/or PC chairs.

# General Guidelines for ACL Reviewing
# Please take a balanced approach when reviewing the papers. On the one hand, we would like to have a solid technical program with high-quality papers describing a complete piece of work; on the other hand, we also want a broad and interesting program, so please keep an open mind when evaluating and recommending the papers assigned to you.

# Please note that a short paper is not a shortened long paper. Instead short papers should have a point that can be made in a few pages and present a focused contribution.

# Following ACL 2019, we suggest that you consult some of the excellent advice from experienced reviewers and conference organizers on the web. In particular:

# Read the excellent blog post by NLP veterans Mirella Lapata, Marco Baroni, Yoav Artzi, Emily Bender, Joel Tetreault, Ani Nenkova, and Tim Baldwin, who compiled their reviewing recommendations for ACL 2017: https://acl2017.wordpress.com/2017/02/23/last-minute-reviewing-advice/
# Nikas Elmqvist from the University of Maryland has great advice on mistakes to avoid when reviewing: https://sites.umiacs.umd.edu/elm/2016/02/01/mistakes-reviewers-make/
# Sample reviews by the NAACL 2018 chairs (note they have a different form):https://naacl2018.wordpress.com/2018/01/20/a-review-form-faq/
# And on the lighter side: https://naacl2018.wordpress.com/2017/12/19/some-holiday-reviewing-advice/
# '''
#     prompt_iclr='''Reviewing a submission: step-by-step
# Summarized in one sentence, a review aims to determine whether a submission will bring sufficient value to the community and contribute new knowledge. The process can be broken down into the following main reviewer tasks:

# Read the paper: It’s important to carefully read through the entire paper, and to look up any related work and citations that will help you comprehensively evaluate it. Be sure to give yourself sufficient time for this step.
# While reading, consider the following:
# Objective of the work: What is the goal of the paper? Is it to better address a known application or problem, draw attention to a new application or problem, or to introduce and/or explain a new theoretical finding? A combination of these? Different objectives will require different considerations as to potential value and impact.
# Strong points: is the submission clear, technically correct, experimentally rigorous, reproducible, does it present novel findings (e.g. theoretically, algorithmically, etc.)?
# Weak points: is it weak in any of the aspects listed in b.?
# Be mindful of potential biases and try to be open-minded about the value and interest a paper can hold for the entire ICLR community, even if it may not be very interesting for you.
# Answer four key questions for yourself, to make a recommendation to Accept or Reject:
# What is the specific question and/or problem tackled by the paper?
# Is the approach well motivated, including being well-placed in the literature?
# Does the paper support the claims? This includes determining if results, whether theoretical or empirical, are correct and if they are scientifically rigorous.
# What is the significance of the work? Does it contribute new knowledge and sufficient value to the community? Note, this does not necessarily require state-of-the-art results. Submissions bring value to the ICLR community when they convincingly demonstrate new, relevant, impactful knowledge (incl., empirical, theoretical, for practitioners, etc).
# Write and submit your initial review, organizing it as follows: 
# Summarize what the paper claims to contribute. Be positive and constructive.
# List strong and weak points of the paper. Be as comprehensive as possible.
# Clearly state your initial recommendation (accept or reject) with one or two key reasons for this choice.
# Provide supporting arguments for your recommendation.
# Ask questions you would like answered by the authors to help you clarify your understanding of the paper and provide the additional evidence you need to be confident in your assessment. 
# Provide additional feedback with the aim to improve the paper. Make it clear that these points are here to help, and not necessarily part of your decision assessment.
# Complete the CoE report: ICLR has adopted the following Code of Ethics (CoE). When submitting your review, you’ll be asked to complete a CoE report for the paper. The report is a simple form with two questions. The first asks whether there is a potential violation of the CoE. The second is relevant only if there is a potential violation and asks the reviewer to explain why there may be a potential violation. In order to answer these questions, it is therefore important that you read the CoE before starting your reviews.
 
# Engage in discussion: The discussion phase at ICLR is different from most conferences in the AI/ML community. During this phase, reviewers, authors and area chairs engage in asynchronous discussion and authors are allowed to revise their submissions to address concerns that arise. It is crucial that you are actively engaged during this phase. Maintain a spirit of openness to changing your initial recommendation (either to a more positive or more negative) rating.
# Borderline paper meeting: Similarly to last year, the ACs are encouraged to (virtually) meet and discuss with reviewers only for borderline cases. ACs will reach out to schedule this meeting. This is to ensure active discussions among reviewers, and well-thought-out decisions. ACs will schedule the meeting and facilitate the discussion. For a productive discussion, it is important to familiarize yourself with other reviewers' feedback prior to the meeting. Please note that we will be leveraging information for reviewers who failed to attend this meeting (excluding emergencies). 
# Provide final recommendation: Update your review, taking into account the new information collected during the discussion phase, and any revisions to the submission. (Note that reviewers can change their reviews after the author response period.)  State your reasoning and what did/didn’t change your recommendation throughout the discussion phase.
#  '''
#     prompt_icml='''Review Form for Main Track
# You will be asked on the review form for each paper and some guidelines on what to consider when answering these questions.  Remember that answering “no” to some questions is typically not grounds for rejection. When writing your review, please keep in mind that after decisions have been made, reviews and meta-reviews of accepted papers and opted-in rejected papers will be made public. 

# Summary: Briefly summarize the paper and its contributions. This is not the place to critique the paper; the authors should generally agree with a well-written summary.
# Strengths and Weaknesses: Please provide a thorough assessment of the strengths and weaknesses of the paper, touching on each of the following dimensions: originality, quality, clarity, and significance. We encourage people to be broad in their definitions of originality and significance. For example, originality may arise from creative combinations of existing ideas, application to a new domain, or removing restrictive assumptions from prior theoretical results. You can incorporate Markdown and Latex into your review. See https://openreview.net/faq.
# Questions: Please list up and carefully describe any questions and suggestions for the authors. Think of the things where a response from the author can change your opinion, clarify a confusion or address a limitation. This can be very important for a productive rebuttal and discussion phase with the authors.
# Limitations: Have the authors adequately addressed the limitations and potential negative societal impact of their work? If not, please include constructive suggestions for improvement. Authors should be rewarded rather than punished for being up front about the limitations of their work and any potential negative societal impact.
# Ethical concerns: If you believe there are ethical issues with this paper, please flag the paper for an ethics review. For guidance on when this is appropriate, please review the ethics guidelines (https://icml.cc/Conferences/2024/PublicationEthics).
# Ethics Review Area: If you flagged this paper for ethics review, what area of expertise would it be most useful for the ethics reviewer to have? Please click all that apply:
# Discrimination / Bias / Fairness Concerns
# Inappropriate Potential Applications & Impact  (e.g., human rights concerns)
# Privacy and Security
# Legal Compliance (e.g., GDPR, copyright, terms of use)
# Research Integrity Issues (e.g., plagiarism)
# Responsible Research Practice (e.g., IRB, documentation, research ethics)
# Other
# Details of Ethics Concerns: If you flagged paper for ethics review, please provide details of your concerns.
# Soundness: Please assign the paper a numerical rating on the following scale to indicate the soundness of the technical claims, experimental and research methodology and on whether the central claims of the paper are adequately supported with evidence.
# 4 excellent
# 3 good
# 2 fair
# 1 poor
# Presentation: Please assign the paper a numerical rating on the following scale to indicate the quality of the presentation. This should take into account the writing style and clarity, as well as contextualization relative to prior work.
# 4 excellent
# 3 good
# 2 fair
# 1 poor
# Contribution: Please assign the paper a numerical rating on the following scale to indicate the quality of the overall contribution this paper makes to the research area being studied. Are the questions being asked important? Does the paper bring a significant originality of ideas and/or execution? Are the results valuable to share with the broader ICML community?
# 4 excellent
# 3 good
# 2 fair
# 1 poor
# Rating: Please provide an "overall score" for this submission. Choices:
# 10: Award quality: Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
# 9: Very Strong Accept: Technically flawless paper with groundbreaking impact on at least one area of AI and excellent impact on multiple areas of AI, with flawless evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
# 8: Strong Accept: Technically strong paper with, with novel ideas, excellent impact on at least one area of AI or high-to-excellent impact on multiple areas of AI, with excellent evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
# 7: Accept: Technically solid paper, with high impact on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
# 6: Weak Accept: Technically solid, moderate-to-high impact paper, with no major concerns with respect to evaluation, resources, reproducibility, ethical considerations.
# 5: Borderline accept: Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. Please use sparingly.
# 4: Borderline reject: Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. Please use sparingly.
# 3: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
# 2: Strong Reject: For instance, a paper with major technical flaws, and/or poor evaluation, limited impact, poor reproducibility and mostly unaddressed ethical considerations.
# 1: Very Strong Reject: For instance, a paper with trivial results or unaddressed ethical considerations
# Confidence:  Please provide a "confidence score" for your assessment of this submission to indicate how confident you are in your evaluation.  Choices
# 5: You are absolutely certain about your assessment. You are very familiar with the related work and checked the math/other details carefully.
# 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
# 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
# 2: You are willing to defend your assessment, but it is quite likely that you did not understand the central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
# 1: Your assessment is an educated guess. The submission is not in your area or the submission was difficult to understand. Math/other details were not carefully checked.
# Code of conduct acknowledgement. While performing my duties as a reviewer (including writing reviews and participating in discussions), I have and will continue to abide by the ICML code of conduct (https://icml.cc/public/CodeOfConduct).
# '''
#     prompt_neurips='''Review Form
# Below is a description of the questions you will be asked on the review form for each paper and some guidelines on what to consider when answering these questions. Feel free to use the NeurIPS paper checklist included in each paper as a tool when preparing your review (some submissions may have the checklist as part of the supplementary materials). Remember that answering “no” to some questions is typically not grounds for rejection. When writing your review, please keep in mind that after decisions have been made, reviews and meta-reviews of accepted papers and opted-in rejected papers will be made public.

# Summary: Briefly summarize the paper and its contributions. This is not the place to critique the paper; the authors should generally agree with a well-written summary.
# Strengths and Weaknesses: Please provide a thorough assessment of the strengths and weaknesses of the paper, touching on each of the following dimensions:
# a. Originality: Are the tasks or methods new? Is the work a novel combination of well-known techniques? (This can be valuable!) Is it clear how this work differs from previous contributions? Is related work adequately cited?
# b. Quality: Is the submission technically sound? Are claims well supported (e.g., by theoretical analysis or experimental results)? Are the methods used appropriate? Is this a complete piece of work or work in progress? Are the authors careful and honest about evaluating both the strengths and weaknesses of their work?
# c. Clarity: Is the submission clearly written? Is it well organized? (If not, please make constructive suggestions for improving its clarity.) Does it adequately inform the reader? (Note that a superbly written paper provides enough information for an expert reader to reproduce its results.)
# d. Significance: Are the results important? Are others (researchers or practitioners) likely to use the ideas or build on them? Does the submission address a difficult task in a better way than previous work? Does it advance the state of the art in a demonstrable way? Does it provide unique data, unique conclusions about existing data, or a unique theoretical or experimental approach?
# You can incorporate Markdown and Latex into your review.  See https://openreview.net/faq.
# Questions: Please list up and carefully describe any questions and suggestions for the authors. Think of the things where a response from the author can change your opinion, clarify a confusion or address a limitation. This can be very important for a productive rebuttal and discussion phase with the authors.  
# Limitations: Have the authors adequately addressed the limitations and potential negative societal impact of their work? If not, please include constructive suggestions for improvement.
# In general, authors should be rewarded rather than punished for being up front about the limitations of their work and any potential negative societal impact. You are encouraged to think through whether any critical points are missing and provide these as feedback for the authors.
# Ethical concerns: If there are ethical issues with this paper, please flag the paper for an ethics review. For guidance on when this is appropriate, please review the NeurIPS ethics guidelines.
# Soundness: Please assign the paper a numerical rating on the following scale to indicate the soundness of the technical claims, experimental and research methodology and on whether the central claims of the paper are adequately supported with evidence.
# 4 excellent
# 3 good
# 2 fair
# 1 poor
# Presentation: Please assign the paper a numerical rating on the following scale to indicate the quality of the presentation. This should take into account the writing style and clarity, as well as contextualization relative to prior work.
# 4 excellent
# 3 good
# 2 fair
# 1 poor
# Contribution: Please assign the paper a numerical rating on the following scale to indicate the quality of the overall contribution this paper makes to the research area being studied. Are the questions being asked important? Does the paper bring a significant originality of ideas and/or execution? Are the results valuable to share with the broader NeurIPS community.
# 4 excellent
# 3 good
# 2 fair
# 1 poor
# Overall: Please provide an "overall score" for this submission. Choices:
# 10: Award quality: Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
# 9: Very Strong Accept: Technically flawless paper with groundbreaking impact on at least one area of AI and excellent impact on multiple areas of AI, with flawless evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
# 8: Strong Accept: Technically strong paper with, with novel ideas, excellent impact on at least one area of AI or high-to-excellent impact on multiple areas of AI, with excellent evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
# 7: Accept: Technically solid paper, with high impact on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
# 6: Weak Accept: Technically solid, moderate-to-high impact paper, with no major concerns with respect to evaluation, resources, reproducibility, ethical considerations.
# 5: Borderline accept: Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. Please use sparingly.
# 4: Borderline reject: Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. Please use sparingly.
# 3: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
# 2: Strong Reject: For instance, a paper with major technical flaws, and/or poor evaluation, limited impact, poor reproducibility and mostly unaddressed ethical considerations.
# 1: Very Strong Reject: For instance, a paper with trivial results or unaddressed ethical considerations
# Confidence:  Please provide a "confidence score" for your assessment of this submission to indicate how confident you are in your evaluation.  Choices
# 5: You are absolutely certain about your assessment. You are very familiar with the related work and checked the math/other details carefully.
# 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
# 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
# 2: You are willing to defend your assessment, but it is quite likely that you did not understand the central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
# 1: Your assessment is an educated guess. The submission is not in your area or the submission was difficult to understand. Math/other details were not carefully checked.
# Code of conduct acknowledgement. While performing my duties as a reviewer (including writing reviews and participating in discussions), I have and will continue to abide by the NeurIPS code of conduct (NeurIPS Code Of Conduct).
#   '''

#     prompt_general = '''
#     As a research paper reviewer, I will critically and rigorously evaluate the uploaded paper, identifying fundamental technical flaws, inconsistencies, and missing elements. The review must go beyond a structured checklist and provide a nuanced, in-depth critique akin to a detailed human review.

# Conceptual flaws must be explicitly discussed, questioning the coherence between objectives, claims, methodology, and experimental results.
# Mathematical descriptions and formalization should be scrutinized line-by-line to check for inaccuracies, inconsistencies, or insufficient justification.
# Logical reasoning gaps must be pointed out, ensuring the paper’s argumentation is sound and conclusions are well-supported.
# Explicitly highlight missing sections (e.g., related work, justification for hyperparameters, ablation studies, ethical considerations).
# Acknowledge strengths where present, but do not dilute the critique. The review should be direct, critical, and constructive.
# Each evaluation category will be assigned a 1 to 5 score, with:

# A clear justification for the score (not just general remarks).
# Specific evidence from the paper (e.g., section numbers, equations, figures).
# Concrete suggestions for improvement, requiring substantial effort from the authors rather than minor refinements.
# 📌 Evaluation Criteria
# 1️⃣ Originality (1-5)
# Does the paper introduce a genuinely novel idea, or is it a minor variation of existing work?
# Is the contribution incremental, redundant, or lacking originality?
# Does the paper convincingly justify why its approach is novel?
# ✅ Strengths: Identify truly novel aspects (if any).
# ❌ Weaknesses: Directly state if the contribution is weak or insufficiently justified. If prior work already covers similar ideas, call this out explicitly.
# 🔹 Improvement Suggestion: Insist on stronger theoretical or empirical differentiation from prior work. If the novelty is weak, suggest alternative problem settings or methodological innovations.

# 2️⃣ Theoretical Soundness & Methodological Rigor (1-5)
# Are theoretical claims well-supported, or are they vague and hand-wavy?
# Are assumptions valid, clearly justified, and non-trivial?
# Do the mathematical formalizations contain inconsistencies, ambiguities, or unstated constraints?
# Are key derivations and proofs complete, or do they skip crucial steps?
# ✅ Strengths: If formalism is clear and rigorous, acknowledge it.
# ❌ Weaknesses: Identify any logical inconsistencies, missing derivations, or incorrect assumptions. If methodology lacks proper justification, call it out explicitly.
# 🔹 Improvement Suggestion: Demand full proof verification, correction of flawed assumptions, or additional theoretical justification.

# 3️⃣ Coherence Between Claims and Experiments (1-5)
# Do the experimental results actually support the paper’s claims?
# Are there hidden contradictions between what the paper argues and what the results demonstrate?
# Does the discussion overstate the significance of results?
# ✅ Strengths: Highlight cases where results match claims.
# ❌ Weaknesses: Point out any instances of cherry-picking, over-exaggeration, or contradictions between methodology and findings.
# 🔹 Improvement Suggestion: Demand revised claims, stronger justification of conclusions, or additional experiments to validate assertions.

# 4️⃣ Experimental Soundness (1-5)
# Are the experimental results statistically robust?
# Are baselines appropriate, strong, and up-to-date?
# Are hyperparameters, datasets, and training details properly reported?
# Does the experimental design support generalizability, or are results cherry-picked?
# ✅ Strengths: Recognize cases where experiments are well-designed.
# ❌ Weaknesses: Identify weak baselines, lack of statistical tests, omitted ablation studies, or missing hyperparameter settings.
# 🔹 Improvement Suggestion: Suggest stronger baselines, more ablation studies, and clearer reporting of all experimental details.

# 5️⃣ Depth and Technical Substance (1-5)
# Does the paper demonstrate deep technical insight, or is it shallow and superficial?
# Is the problem approached from multiple angles, or is the exploration surface-level?
# ✅ Strengths: Acknowledge comprehensive exploration.
# ❌ Weaknesses: Call out shallow reasoning, oversimplifications, or lack of depth.
# 🔹 Improvement Suggestion: Suggest more rigorous technical exploration, alternative perspectives, or additional theoretical backing.

# 6️⃣ Clarity & Presentation (1-5)
# Are key concepts well-explained, or does the paper assume too much background knowledge?
# Are notation and figures clear and self-contained?
# Are there ambiguities in definitions or unclear sections?
# ✅ Strengths: Recognize well-structured explanations.
# ❌ Weaknesses: Point out vague writing, inconsistent notation, or unexplained jargon.
# 🔹 Improvement Suggestion: Suggest rewriting unclear sections, adding more intuitive explanations, or improving figures.

# 7️⃣ Reproducibility & Transparency (1-5)
# Can others fully reproduce the results?
# Are code, datasets, and hyperparameters provided?
# Are crucial experimental details missing or ambiguous?
# ✅ Strengths: If reproducibility is strong, acknowledge it.
# ❌ Weaknesses: Criticize missing details, lack of dataset/code access, or vague descriptions.
# 🔹 Improvement Suggestion: Demand open-source code, full dataset access, and detailed hyperparameter reporting.

# 8️⃣ Missing Elements (Standalone Section)
# Beyond scoring, explicitly identify if any key sections are absent, such as:

# Missing Related Work section.
# No explanation of hyperparameters or training details.
# No ablation studies or statistical significance tests.
# If something critical is missing, call it out explicitly rather than relying on low scores.

#     '''

    # match conference.lower():
    #     case "neurips":
    #         return prompt_neurips
    #     case "iclr":
    #         return prompt_iclr
    #     case "acl":
    #         return prompt_acl
    #     case "icml":
    #         return prompt_icml
    #     case _:
    #         return prompt_general

def get_student_reviews(conference,title, file_path):
    # prompt = get_conference_criteria(conference) +'''\n\n
    # return the output in form of json:
    # {
    #     'final_score':'0/10',
    #     'decision':'Accept/Reject',
    #     'review':[{'content':'review of the paper','strengths':['strength1 of the paper','strength2 of the paper'],'weaknesses':['weakness1 of the paper','weakness2 of the paper'] }],
    # }    
    # '''
    
    prompt = get_conference_criteria(conference,title)
    file = genai.upload_file(file_path, display_name="My Document")
    
    
    response = model.generate_content(
        [prompt, file]
    )
    print(response.text)
    data = response.text.split("```json")[1].strip().split("```")[0]
    data = json.loads(data)

    return data 



