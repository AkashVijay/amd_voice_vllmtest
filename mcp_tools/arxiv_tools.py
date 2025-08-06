from fastmcp import FastMCP,Context
import requests
import feedparser
from typing import List, Dict
from datetime import datetime,timedelta,timezone
import xml.etree.ElementTree as ET
from sqlalchemy.orm import sessionmaker
from db.models import Paper, engine


Session = sessionmaker(bind=engine)

def initialize_tools(mcp: FastMCP):
    
    # Search prompt
    @mcp.tool() 
    def search_arxiv(query: str) -> Dict:
        """_summary_

        Args:
            query (str): _description_

        Returns:
            Dict: _description_
        """
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=4"
        try:
            response = requests.get(url)
            feed = feedparser.parse(response.text)

            papers = []
            for entry in feed.entries:
           
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_iso = datetime(*entry.published_parsed[:6]).isoformat() + "Z"
                else:
                    published_iso = "Unknown"

                papers.append({
                    "title": entry.title,
                    "published": published_iso, 
                    "abstract": entry.summary,
                    "authors": [author.name for author in entry.authors],
                    "link": entry.link,
                })

            return {"papers": papers}
        except Exception as e:
            return {"error": str(e)}
    
        
    #summarize
    @mcp.tool()
    def summarize_abstract_phd(abstract: str):
        """_summary_

        Args:
            abstract (str): _description_

        Returns:
            _type_: _description_
        """
        return (
            f"Summarize the following abstract in 5 sentences. Include the key findings and significance, technical terms, and future work. Explain it as if I'm a PhD student:\n\n{abstract}")

    @mcp.tool()
    def summarize_abstract_college(abstract: str):
        """_summary_

        Args:
            abstract (str): _description_

        Returns:
            _type_: _description_
        """
        return (
            f"Explain this abstract to me like I am a college student studying the topic. Explain it in 7 sentences. Focus on main ideas, significance, and technical terms:\n\n{abstract}"
        )

    @mcp.tool()
    def summarize_abstract_eli10(abstract: str):
        """_summary_

        Args:
            abstract (str): _description_

        Returns:
            _type_: _description_
        """
        return (
            f"Explain this abstract to me like I am ten years old in 5 sentences. Use simple language, analogies, and examples for it to be universally understood:\n\n{abstract}"
        )
    #Compare
    @mcp.tool()
    def compare_abstracts_tool(abstract1: str, abstract2: str):
        """_summary_

        Args:
            abstract1 (str): _description_
            abstract2 (str): _description_

        Returns:
            _type_: _description_
        """
        return (
                f"Compare the following two research abstracts. Do four sentences for each abstract for each section.\n"
                f"Key differences:\n"
                f"- Research goals\n"
                f"- Techniques used\n"
                f"- Application focus\n"
                f"- Experimental setup\n\n"
                f"Summarize the contrasts in goals and outcomes."
                f"Abstract 1:\n{abstract1}\n\n"
                f"Abstract 2:\n{abstract2}"
            )

    #Search by date
    @mcp.tool()
    def filter_by_date(papers: List[Dict], year_cutoff: int = 2010) -> Dict:
        """_summary_

        Args:
            papers (List[Dict]): _description_
            year_cutoff (int, optional): _description_. Defaults to 2010.

        Returns:
            Dict: _description_
        """
        filtered_papers = []

        for paper in papers:
            try:
                published = paper.get("published") or paper.get("published_date")
                if "T" in published:
                    pub_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
                else:
                    pub_date = datetime.strptime(published, "%Y-%m-%d")
                if pub_date.year > year_cutoff:
                    filtered_papers.append(paper)
            except Exception as e:
                continue
        return {"filtered": filtered_papers}
    
    #search by author
    @mcp.tool()
    def search_by_author(author: str) -> Dict:
        """_summary_

        Args:
            author (str): _description_

        Returns:
            Dict: _description_
        """
        encoded_author = author.replace(" ", "+")
        url = f"http://export.arxiv.org/api/query?search_query=au:{encoded_author}&start=0&max_results=5"

        try:
            response = requests.get(url)
            feed = feedparser.parse(response.text)
            papers = []

            for entry in feed.entries:
                published = datetime(*entry.published_parsed[:5]).isoformat() + "Z"
                papers.append({
                    "title": entry.title,
                    "abstract": entry.summary,
                    "link": entry.link,
                    "authors": [author.name for author in entry.authors],
                    "published": published,
                })

            return {"papers": papers}

        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def save_paper(title: str, summary: str, published: str):
        """_summary_

        Args:
            title (str): _description_
            summary (str): _description_
            published (str): _description_

        Returns:
            _type_: _description_
        """
        session = Session()
        try:
            paper = Paper(
                title=title,
                summary=summary,
                published=datetime.fromisoformat(published.replace("Z", "")),
            )
            session.add(paper)
            session.commit()
            return {"status": "saved"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            session.close()

    @mcp.tool()
    def get_saved_papers():
        """_summary_

        Returns:
            _type_: _description_
        """
        session = Session()
        try:
            papers = session.query(Paper).all()
            return {
                "papers": [
                    {
                        "title": p.title,
                        "summary": p.summary,
                        "published": p.published.isoformat(),
                    }
                    for p in papers
                ]
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            session.close()

    @mcp.tool()
    def delete_all_papers():
        """_summary_

        Returns:
            _type_: _description_
        """
        session = Session()
        try:
            session.query(Paper).delete()
            session.commit()
            return {"status": "all_deleted"}
        finally:
            session.close()

#extra tools


# @mcp.tool()
    # def get_recent_papers(topic: str, months: int = 12) -> Dict:
    #     url = f"http://export.arxiv.org/api/query?search_query=all:{topic.replace(' ', '+')}&start=0&max_results=8"

    #     try:
    #         response = requests.get(url)
    #         feed = feedparser.parse(response.text)
    #         cutoff_date = datetime.now(timezone.utc) - timedelta(days=30 * months)
    #         papers = []

    #         for entry in feed.entries:
    #             published = datetime(*entry.published_parsed[:6])
    #             if published >= cutoff_date:
    #                 papers.append({
    #                     "title": entry.title,
    #                     "link": entry.link,
    #                     "published": published.isoformat() + "Z",
    #                 })

    #         return {"papers": papers}

    #     except Exception as e:
    #         return {"error": str(e)}