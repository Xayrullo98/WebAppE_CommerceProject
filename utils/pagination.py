import math

from fastapi import HTTPException

# def pagination(form, page, limit):
#     if page < 0 or limit < 0:
#         raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
#     elif page and limit:
#         return {"current_page": page, "limit": limit, "pages": math.ceil(form.count() / limit),
#             "data": form.offset((page - 1) * limit).limit(limit).all()}
#     else:
#         return {"data": form.all()}

def pagination(form, page, limit):
    if page == 1 or page < 1:
        offset = 0
        return {"current_page": page, "limit": limit, "pages": math.ceil(form.count() / limit),
                "data": form.offset((0) * limit).limit(limit).all()}
    else:
        offset = (page - 1) * limit
        return {"current_page": page, "limit": limit, "pages": math.ceil(form.count() / limit),
                "data": form.offset((page - 1) * limit).limit(limit).all()}



NAQD = 'NAQD'
NASIYA = 'NASIYA'