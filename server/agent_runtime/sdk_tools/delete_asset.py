"""SDK MCP tool for deleting a project asset and its project artifacts."""

from __future__ import annotations

from typing import Any

from claude_agent_sdk import tool

from server.media_tools.context import ToolContext, tool_outcome_response, tool_services
from server.tool_runtime import ASSET_TABLES as _TABLES
from server.tool_runtime import (
    DeleteAssetRequest,
    ToolOutcome,
    ToolProblem,
    ToolRequest,
    delete_asset,
)


def delete_asset_tool(ctx: ToolContext):
    @tool(
        "delete_asset",
        "Delete one project asset and its project artifacts. Does not affect the global asset library.",
        {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "enum": list(_TABLES),
                    "description": "Asset table: characters / scenes / props / products",
                },
                "name": {"type": "string", "description": "Existing project asset name"},
            },
            "required": ["table", "name"],
        },
    )
    async def _handler(args: dict[str, Any]) -> dict[str, Any]:
        try:
            request = DeleteAssetRequest.model_validate(args)
        except ValueError as exc:
            outcome = ToolOutcome(problem=ToolProblem("invalid_request", str(exc)))
        else:
            outcome = await delete_asset(ToolRequest(request), ctx.scope, ctx.caller, tool_services(ctx))
        return tool_outcome_response("asset_delete", outcome)

    return _handler


__all__ = ["delete_asset_tool"]
