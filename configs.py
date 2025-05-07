
def get_llm_tools():
    return [
        {
            "name": "extract_company_info",
            "description": "Extract detailed information about companies mentioned in text",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text containing company mentions to analyze"
                    }
                },
                "required": ["text"]
            },
            "output_schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Company name"
                        },
                        "website": {
                            "type": "string",
                            "description": "Company's official website URL"
                        },
                        "sector": {
                            "type": "string",
                            "description": "Business sector or industry the company operates in"
                        },
                        "location": {
                            "type": "string",
                            "description": "Company headquarters location"
                        },
                        "description": {
                            "type": "string",
                            "description": "Brief description of what the company does"
                        },
                        "key_people": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Name of key person"
                                    },
                                    "title": {
                                        "type": "string",
                                        "description": "Role or title of the person"
                                    }
                                }
                            },
                            "description": "Key executives, founders, or important people in the company"
                        },
                        "competitors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Competitor company name"
                                    },
                                    "strength": {
                                        "type": "string",
                                        "enum": ["primary", "secondary", "tertiary"],
                                        "description": "Competitive relationship strength"
                                    },
                                    "sector_overlap": {
                                        "type": "string",
                                        "description": "Areas where the companies compete"
                                    }
                                }
                            },
                            "description": "Detailed analysis of company competitors"
                        }
                    },
                    "required": ["name", "website", "sector", "location", "description", "key_people", "competitors"]
                }
            }
        },
    ]


def get_sysprompt():
    return """You are a specialized named entity recognition system focused on identifying and extracting detailed company information from text. 
        Extract ALL companies mentioned in the text and use the extract_company_info tool to return structured data for each company.
        Be thorough and extract every company mentioned, even if you only have partial information. 
        Make reasonable inferences for missing information but clearly indicate when information is inferred.
        
        If the text does not contain any companies or company-related information, that's completely fine.
        In such cases, it's appropriate to return nothing or indicate that no company information was found in the text."""
