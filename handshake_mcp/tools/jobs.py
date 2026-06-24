"""Job search, details, apply, and bookmark tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import api_delete, api_post, gql

_JOB_FIELDS = """
  id
  title
  description
  remote
  createdAt
  startDate
  employer {
    id
    name
    website
    location { name }
    industry { name }
  }
  jobType { name }
  employmentType { name }
  salaryType { name }
"""

_SEARCH_QUERY = """
query JobSearch($first: Int) {
  jobSearch(first: $first) {
    totalCount
    nodes {
      job {
        """ + _JOB_FIELDS + """
      }
    }
  }
}
"""

_GET_JOB_QUERY = """
query GetJob($id: ID!) {
  job(id: $id) {
    """ + _JOB_FIELDS + """
  }
}
"""


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_search_jobs(per_page: int = 20) -> dict:
        """Search for recommended jobs and internships on Handshake.

        Returns your personalized job feed — postings matched to your profile,
        school, and preferences. Use hs_get_job to get the full description
        for any posting.

        Args:
            per_page: Number of results to return (max 50).
        """
        data = await gql(_SEARCH_QUERY, {"first": min(per_page, 50)})
        jobs = data["jobSearch"]
        # Flatten: extract job object from each search result node
        jobs["results"] = [node["job"] for node in jobs.pop("nodes", [])]
        return jobs

    @mcp.tool()
    async def hs_get_job(job_id: str) -> dict:
        """Get full details of a Handshake job posting.

        Includes description, employer, job type, remote status, salary type,
        and start date.

        Args:
            job_id: Handshake job ID (from hs_search_jobs results).
        """
        data = await gql(_GET_JOB_QUERY, {"id": job_id})
        return data["job"]

    @mcp.tool()
    async def hs_apply(
        job_id: str,
        document_ids: list[int] | None = None,
    ) -> dict:
        """Submit a Handshake application for a job.

        Call hs_get_job first to confirm the job accepts Handshake applications.

        Args:
            job_id: Handshake job ID.
            document_ids: IDs of documents to attach (resume, cover letter).
                Retrieve IDs with hs_get_documents.
        """
        body: dict = {}
        if document_ids:
            body["document_ids"] = document_ids
        return await api_post(f"/postings/{job_id}/apply", body)

    @mcp.tool()
    async def hs_save_job(job_id: str) -> dict:
        """Bookmark a job posting to your Handshake saved-jobs list.

        Args:
            job_id: Handshake job ID.
        """
        return await api_post("/saved_jobs", {"posting_id": int(job_id)})

    @mcp.tool()
    async def hs_unsave_job(saved_job_id: str) -> dict:
        """Remove a job from your Handshake saved-jobs list.

        Args:
            saved_job_id: Saved-job record ID from hs_get_saved_jobs.
                This is different from the job ID.
        """
        return await api_delete(f"/saved_jobs/{saved_job_id}")

    @mcp.tool()
    async def hs_get_saved_jobs(page: int = 1, per_page: int = 25) -> dict:
        """List all jobs you have bookmarked on Handshake.

        Args:
            page: Page number (starts at 1).
            per_page: Results per page.
        """
        return await api_post("/saved_jobs/search", {"page": page, "per_page": per_page})
