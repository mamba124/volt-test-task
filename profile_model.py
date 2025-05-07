from pydantic import BaseModel, Field
from typing import List, Literal


class KeyPerson(BaseModel):
    """Model representing a key person in a company."""
    name: str = Field(description="Name of key person")
    title: str = Field(description="Role or title of the person")


class Competitor(BaseModel):
    """Model representing a company competitor."""
    name: str = Field(description="Competitor company name")
    strength: Literal["primary", "secondary", "tertiary"] = Field(
        description="Competitive relationship strength"
    )
    sector_overlap: str = Field(description="Areas where the companies compete")


class CompanyInfo(BaseModel):
    """Model representing detailed information about a company."""
    name: str = Field(description="Company name")
    website: str = Field(description="Company's official website URL")
    sector: str = Field(description="Business sector or industry the company operates in")
    location: str = Field(description="Company headquarters location")
    description: str = Field(description="Brief description of what the company does")
    key_people: List[KeyPerson] = Field(
        description="Key executives, founders, or important people in the company"
    )
    competitors: List[Competitor] = Field(
        description="Detailed analysis of company competitors"
    )


class CompanyInfoResponse(BaseModel):
    """Model representing the entire response from the extract_company_info tool."""
    companies: List[CompanyInfo]
