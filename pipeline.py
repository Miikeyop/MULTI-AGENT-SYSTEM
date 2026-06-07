from agents import web_agent, reader_agent, report_chain, critic_chain
  
def result_report_pipeline(topic:str)->dict:

    state={}

    print("\n"+"-"*50)
    print("web agent is working")
    print("-"*50)
    #web agent/search agent

    search_agent=web_agent()
    search_result=search_agent.invoke({
        "messages":[{
            "role":"user",
            "content":f"Find the recent  reliable and detailed information about: {topic}"
        }]
    })
    state["search_result"]=search_result["messages"][-1].content
    print("\nsearch result\n",state["search_result"])

    #reader agent
    print("\n"+"-"*50)
    print("reader agent is working")
    print("-"*50)

    reader=reader_agent()
    reader_result = reader.invoke({
    "messages": [{
        "role": "user",
        "content": f"""
Topic:
{topic}

Search Result:
{state["search_result"]}

Select the most relevant URL from the search result.
Use scrape_url tool to read that URL.
Return detailed research notes.
"""
    }]
})
    state["reader_result"]=reader_result["messages"][-1].content
    print("\nreader result\n",state["reader_result"])



    print("\n"+"-"*50)
    print("report is working")
    print("-"*50)
    #chaining
    research_combined = (
    f"SEARCH RESULTS : \n {state['search_result']} \n\n"
    f"DETAILED SCRAPED CONTENT : \n {state['reader_result']}")

    state["report"]=report_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\nfinal report\n",state["report"])

    print("\n"+"-"*50)
    print("reviewing report is working")
    print("-"*50)

    #crritic 
    state["feedback"]=critic_chain.invoke({
        "report":state["report"],

    })
    
    print("\nfeedback\n",state["feedback"])


    return state
 


if __name__=="__main__":
    topic=input("\nEnter the topic you want to research and generate report on: \n")
    result_report_pipeline(topic)







