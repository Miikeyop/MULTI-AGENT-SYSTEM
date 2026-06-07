from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()
from tool import web_search,scrape_url


llm=ChatMistralAI(model="mistral-medium-3-5")
parser=StrOutputParser()
def web_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

def reader_agent():
     return create_agent(
        model=llm,
        tools=[scrape_url]
    )

report_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert report writer.

Your job is to create a clear, well-structured, and professional report using the topic and research provided by the user.

Rules:
- Use only the research provided by the user.
- Do not add fake facts.
- If some information is missing, mention it clearly.
- Write in simple English.
- Organize the report with proper headings.
- Make the report easy to read.
- Keep the tone professional.
"""
    ),
    (
        "human",
        """
Create a detailed report on the following topic.

Topic:
{topic}

Research Material:
{research}

Report Format:
1. Title
2. Introduction
3. Key Points
4. Detailed Explanation
5. Benefits / Importance
6. Challenges / Limitations
7. Conclusion
"""
    )
])

report_chain=report_prompt|llm|parser

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert report evaluator and critic.

Your job is to review a report carefully and give honest feedback.

Evaluation rules:
- Check if the report matches the given topic.
- Check if the report uses the provided research properly.
- Check clarity, structure, depth, accuracy, and usefulness.
- Do not be overly positive.
- Do not rewrite the full report.
- Give a score out of 10.
- Highlight weak areas clearly.
- Suggest practical improvements.
- Use simple English.
"""
    ),
    (
        "human",
        """
Evaluate the following report.


Report:
{report}

Give feedback in this format:

1. Overall Score:
Give score out of 10.

2. Short Review:
Write 3-5 lines about report quality.

3. Strengths:
Mention what is good in the report.

4. Weak Areas:
Mention what is missing or weak.

5. Areas of Improvement:
Give clear suggestions to improve the report.

6. Final Recommendation:
Say whether the report is:
- Excellent
- Good
- Average
- Needs Improvement
"""
    )
])

critic_chain=critic_prompt|llm|parser