# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict
# from datetime import datetime
# from services.audit_service import AuditService
# from services.ai_service import AIService
# from services.db_service import DBService

# router = APIRouter(prefix="/api/audit", tags=["Auditor"])


# class AuditRequest(BaseModel):
#     data: List[Dict]


# @router.post("/scan")
# async def scan_data(req: AuditRequest):
#     try:
#         stats_report, raw_summary = AuditService.perform_statistical_audit(req.data)

#         ai_summary = await AIService.get_audit_summary(stats_report, raw_summary)




from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from services.audit_service import AuditService
from services.ai_service import AIService
from services.db_service import DBService

router = APIRouter(prefix="/api/audit", tags=["Auditor"])


class AuditRequest(BaseModel):
    data: List[Dict]


@router.post("/scan")
async def scan_data(req: AuditRequest):
    try:
        stats_report, raw_summary = AuditService.perform_statistical_audit(req.data)

        ai_summary = await AIService.get_audit_summary(stats_report, raw_summary)

        audit_doc = {
            "timestamp": datetime.utcnow(),
            "stats": stats_report,
            "ai_analysis": ai_summary,
        }
        db_id = await DBService.save_report(audit_doc)

        return {
            "status": "success",
            "report_id": db_id,
            "statistics": stats_report,
            "ai_analysis": ai_summary,
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
