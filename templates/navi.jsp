<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>snowball</title>
    <style>
        .top-links {
            display: flex;
            justify-content: space-between;
            background-color: #f0f0f0;
            padding: 10px;
        }
        .top-link {
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <a href="/"><img src="{{ url_for('static', filename='img/logo.jpg')}}" width="200" alt="None"></a>
    <div class="top-links">
        <form class = "grid" action = "/link1" method = "POST"><a href="/link1" class="top-link">RCM</a></form>
        <form class = "grid" action = "/link2" method = "POST"><a href="/link2" class="top-link">검토요청</a></form>
        <form class = "grid" action = "/link3" method = "POST"><a href="/link3" class="top-link">양식받기</a></form>
        <form class = "grid" action = "/link4" method = "POST"><a href="/link4" class="top-link">교육영상</a></form>
    </div>
</body>
</html>