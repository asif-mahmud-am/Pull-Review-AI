from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    login: str
    id: int
    node_id: str = Field(alias="node_id")
    avatar_url: str = Field(alias="avatar_url")


    class Config:
        populate_by_name = True


class Repo(BaseModel):
    id: int
    node_id: str = Field(alias="node_id")
    name: str
    full_name: str = Field(alias="full_name")
    private: bool
    html_url: str = Field(alias="html_url")
    description: Optional[str] = None

    class Config:
        populate_by_name = True

class Base(BaseModel):
    label: str
    ref: str
    sha: str
    user: User
    repo: Repo

    class Config:
        populate_by_name = True

class PullRequest(BaseModel):
    url: str
    html_url: str = Field(alias="html_url")
    diff_url: str = Field(alias="diff_url")
    title: str
    body: Optional[str] = None
    state: str
    number: int
    user: User 
    base: Base 

    class Config:
        populate_by_name = True

class Repository(BaseModel):
    full_name: str = Field(alias="full_name")

    class Config:
        populate_by_name = True

class PullRequestEvent(BaseModel):
    action: str
    pull_request: PullRequest = Field(alias="pull_request")
    repository: Repository = Field(alias="repository")

    class Config:
        populate_by_name = True

    def get_pull_request_number(self):
        return self.pull_request.number

    def get_diff_url(self):
        return self.pull_request.diff_url

    def get_repo_full_name(self):
        return self.repository.full_name

    def get_pull_request_title(self):
        return self.pull_request.title