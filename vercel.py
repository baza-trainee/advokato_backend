# from sqlalchemy import select
# from src.contacts.models import Contacts

# from src.database import get_async_session


# async def customlifespan():
#     print("lifespan start")
#     session = get_async_session()
#     async for s in session:
#         async with s.begin():
#             query = select(Contacts)
#             result = await s.execute(query)
#             contacts = result.scalars().first()
#             if not contacts:
#                 contacts = Contacts(
#                     address="вул.Бульварно-Кудрявська, 2", phone="+38(097)290-79-40"
#                 )
#                 s.add(contacts)
#                 await s.commit()
#     print("lifespan end")


# from src.main import app

# from fastapi import __version__
# from fastapi.responses import HTMLResponse


# html = (
#     """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>FastAPI on Vercel</title>
#     <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
#     <style>
#         body {
#             font-family: 'Arial', sans-serif;
#             margin: 0;
#             padding: 0;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             height: 100vh;
#             background-color: #f8f9fa; /* Light gray background */
#         }

#         .container {
#             background-color: #ffffff; /* White container background */
#             padding: 40px; /* Increased padding for a larger container */
#             border-radius: 12px; /* Rounded corners */
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             text-align: center;
#         }

#         h1 {
#             color: #343a40; /* Dark gray text */
#             font-size: 32px; /* Increased font size */
#         }

#         ul {
#             list-style-type: none;
#             padding: 0;
#         }

#         li {
#             margin: 15px 0; /* Increased margin */
#         }

#         a {
#             color: #007bff; /* Business blue link color */
#             text-decoration: none;
#         }

#         p {
#             color: #6c757d; /* Medium gray text */
#         }
#     </style>"""
#     + f"""
# </head>
# <body>
#     <div class="container">
#         <h1>Hello from FastAPI@{__version__} app</h1>
#         <h3>get started?</h3>
#         <ul>
#             <li><h2><a href="/docs">/docs</a></h2></li>
#             <li><h2><a href="/redoc">/redoc</a></h2></li>
#         </ul>
#         <p>:)</p>
#     </div>
# </body>
# </html>
# """
# )


# @app.get("/", include_in_schema=False)
# async def root():
#     return HTMLResponse(html)
from calendarapi.wsgi import app