from pydantic import BaseModel, Field
from typing import Optional, Dict, List


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

class PRUser(BaseModel):
    login: str

class PullRequestInput(BaseModel):
    title: str
    body: str
    user: PRUser
    url: str
    diff_url: str
    number: int

class RepositoryInput(BaseModel):
    description: str

class PRPayload(BaseModel):
    pull_request: PullRequestInput
    repository: RepositoryInput

class PRFileInfo(BaseModel):
    pr_file_name: str
    pr_file_status: str
    pr_file_additions: int
    pr_file_deletions: int
    pr_file_changes: int
    pr_file_content_before: str
    pr_file_content_after: str
    pr_file_diff: str
    pr_file_blob_url: str


class PRPayloadV2(BaseModel):
    pull_request: dict  # Use dict for now, can be further typed if needed
    # The structure of pull_request matches the provided JSON