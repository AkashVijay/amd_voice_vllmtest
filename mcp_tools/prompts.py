from urllib import response
from fastmcp import FastMCP, Context

def check_prompts(mcp: FastMCP):


    @mcp.prompt
    def search_topic(ctx: Context, topic: str):
        result = ctx.call("search_arxiv", {"query": topic})
        papers = result.get("papers", [])

        if not papers:
            return {"display": "No papers found."}

        ctx.set("recent_papers", papers)
        
        output = "\n\n".join(
            f"**{p['title']}**\n"
            f"Published: {p['published']}\n"
            f"Authors: {', '.join(p['authors'])}\n"
            f"Abstract: {p['abstract']}\n"
            f"[Link]({p['link']})"
            for p in papers)

        return {"display": f"```\n{output}\n```"}
    # def search_topic(ctx: Context, topic: str):
    #     ctx.call("search_arxiv", {"query": topic})
    #     return f"Searching for recent papers on **{topic}**..."
    
    @mcp.prompt
    def summarize_college(ctx: Context, index: int):
        papers = ctx.get("recent_papers", [])
        if not (1 <= index <= len(papers)):
            return {"display": f"Invalid paper index. Please choose between 1 and {len(papers)}."}
        abstract = papers[index - 1]["abstract"]
        prompt = ctx.call("summarize_abstract_phd", {"abstract": abstract})
        result = ctx.llm(prompt)
        return {"display": result}

    @mcp.prompt
    def summarize_college(ctx: Context, index: int):
        papers = ctx.get("recent_papers", [])
        if not (1 <= index <= len(papers)):
            return {"display": f"Invalid paper index. Please choose between 1 and {len(papers)}."}
        abstract = papers[index - 1]["abstract"]
        prompt = ctx.call("summarize_abstract_college", {"abstract": abstract})
        result = ctx.llm(prompt)
        return {"display": result}

    @mcp.prompt
    def summarize_college(ctx: Context, index: int):
        papers = ctx.get("recent_papers", [])
        if not (1 <= index <= len(papers)):
            return {"display": f"Invalid paper index. Please choose between 1 and {len(papers)}."}
        abstract = papers[index - 1]["abstract"]
        prompt = ctx.call("summarize_abstract_eli10", {"abstract": abstract})
        result = ctx.llm(prompt)
        return {"display": result}
    
    @mcp.prompt
    def filter_papers_after_year(ctx: Context, papers: list, year: int):
        ctx.call("filter_by_date", {"papers": papers, "year_cutoff": year})
        return f"Papers published after {year}:"
    
    @mcp.prompt
    def find_papers_by_author(ctx: Context, author: str):
        result = ctx.call("search_by_author", {"author": author})
        papers = result.get("papers", [])

        if not papers:
            return {"display": "No papers found."}

        ctx.set("recent_papers", papers)
        
        output = "\n\n".join(
            f"**{p['title']}**\n"
            f"Published: {p['published']}\n"
            f"Authors: {', '.join(p['authors'])}\n"
            f"Abstract: {p['abstract']}\n"
            f"[Link]({p['link']})"
            for p in papers)

        return {"display": f"```\n{output}\n```"}

    @mcp.prompt
    def compare_abstracts(ctx: Context, index1: int, index2: int):
        papers = ctx.get("recent_papers", [])
        if not (1 <= index1 <= len(papers)) or not (1 <= index2 <= len(papers)):
            return {"display": f"Invalid indices. Choose between 1 and {len(papers)}."}

        abstract1 = papers[index1 - 1]["abstract"]
        abstract2 = papers[index2 - 1]["abstract"]

        prompt = ctx.call("compare_abstracts_tool", {
            "abstract1": abstract1,
            "abstract2": abstract2
        })

        result = ctx.llm(prompt)
        return {"display": result}
    
    @mcp.prompt
    def expand_topic(topic: str):
        return (
            f"I'm interested in the research topic '{topic}'. Suggest more specific or emerging subtopics within this field."
        )
