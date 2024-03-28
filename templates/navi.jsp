<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top Links</title>
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
    <div class="top-links">
        <form class = "grid" action = "/link1" method = "POST"><a href="/link1" class="top-link">PBC</a></form>
        <form class = "grid" action = "/link2" method = "POST"><a href="/link2" class="top-link">RCM</a></form>
        <form class = "grid" action = "/link3" method = "POST"><a href="/link3" class="top-link">Paper</a></form>
    </div>
</body>
</html>