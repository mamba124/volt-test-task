import anthropic
from configs import get_llm_tools, get_sysprompt
import os
import json
from profile_model import CompanyInfoResponse

API_KEY = os.environ['ANTHROPIC_API_KEY']
LLM = os.environ['LLM']
DEFAULT_FILE_PATH = "companies.json"


class ClaudeNER:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=API_KEY)
        self.model = LLM

    def get_entities(self, text):
        tools = get_llm_tools()
        SYSTEMPROMPT = get_sysprompt()
        
        response = self.client.messages.create(
                        model=self.model,
                        max_tokens=2048,
                        system=SYSTEMPROMPT,
                        tools=tools,
                        tool_choice={"type": "tool", "name": "extract_company_info"},
                        messages=[
                            {"role": "user", "content": f"Extract all company information from this text: {text}"}
                        ]
                    )
        return response.json()
        
    def parse_entities(self, response):
        tool_outputs = []
        for message in response.get("messages", []):
            if message.get("role") == "assistant":
                for content_item in message.get("content", []):
                    if content_item.get("type") == "tool_use" and content_item.get("name") == "extract_company_info":
                        tool_output = json.loads(content_item.get("input", {}).get("text", "{}"))
                        tool_outputs.append(tool_output)
        
        if tool_outputs:
            company_info_response = CompanyInfoResponse(companies=tool_outputs[0])
            return company_info_response.companies
        else:
            return []


def extract_company_info(text: str):
    engine = ClaudeNER()
    company_info_response_list = engine.get_entities(text)
    return company_info_response_list

    
def run(text_sample):
    result = extract_company_info(text_sample)
    
    for company in result.companies:
        print(f"Company: {company.name}")
        print(f"Website: {company.website}")
        print(f"Sector: {company.sector}")
        print(f"Key people:")
        for person in company.key_people:
            print(f"  - {person.name}: {person.title}")

    json_data = result.model_dump_json(indent=4)
    
    with open(DEFAULT_FILE_PATH, 'w', encoding='utf-8') as ftp:
        ftp.write(json_data)    


if __name__ == "__main__":
    text_sample = """
        First, I wanted to touch on a few things before we go deeper into the Phoenix Tailings discussion.
        We've got some interesting developments in the sector. So, MP Materials has finally completed its acquisition of Lynas Rare Earths' processing facility in Texas.
        Big news. I've been talking to Eric Zhang, their CEO, and it seems like they're gearing up to ramp up production, focusing primarily on neodymium and praseodymium. 
        The demand for these metals is still through the roof.
        But that's something we need to keep in mind as we look at Phoenix Tailings. 
        They're in the same space, though their approach is a bit different. 
        We all know about their focus on recycling mining tailings. 
        I'm particularly curious about how Phoenix plans to compete with these traditional players like MP Materials and Lynas, especially with their environmentally friendly claims.
        """
    run(text_sample)