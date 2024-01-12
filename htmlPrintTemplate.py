head = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            font-size: 27px;
        }

        td,
        th {
            border-bottom: 1px solid #000;
            text-align: left;
            padding: 8px;
        }
    </style>
</head>

<body>
'''

template = '''
<table>
        <tr">
            <th style="border: 0;">ID: {id}</th>
            <th style="border: 0;"></th>
            <th style="border: 0;"></th>
        </tr>
        <tr>
            <th style="border-top: 0; font-size: large; padding-top: 0; font-weight: 500;">{datetime} - {payment_method}</th>
            <th style="border-top: 0; font-size: large; padding-top: 0;"></th>
            <th style="border-top: 0; font-size: large; padding-top: 0;"></th>
        </tr>
        <tr>
            <th>Món ăn</th>
            <th>Đơn giá</th>
            <th>Tổng</th>
        </tr>
        {payment_list}
        <tr>
            <td style="border-right: none;"></td>
            <td style="text-align: right; border-left: none; font-weight: 600;">Giảm giá</td>
            <td>{discount}</td>
        </tr>
        <tr>
            <td style="border-right: none;"></td>
            <td style="text-align: right; border-left: none; font-weight: 600;">Tổng đơn</td>
            <td>{sum}</td>
        </tr>
    </table>
</body>
</html>
'''