       
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

BOOKINGS = []

HTML_PAGE = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Катерина • Манікюр Требухів (@trebukhiv_nails)</title>
  <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600;700&family=Playfair+Display:ital,wght@0,600;1,500&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Comfortaa', sans-serif;
      background: linear-gradient(145deg, #ffe4ef 0%, #ffd1e6 45%, #ffb6d9 100%);
      min-height: 100vh;
      color: #4a102b;
      padding: 2rem 1rem 3rem;
    }
    .container {
      max-width: 880px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(12px);
      padding: 2.3rem 1.5rem;
      border-radius: 28px;
      border: 2px solid #ffffff;
      box-shadow: 0 14px 32px rgba(219, 39, 119, 0.18);
      margin-bottom: 1.8rem;
    }
    .location-tag {
      display: inline-block;
      background: #fce7f3;
      color: #9d174d;
      font-weight: 700;
      font-size: 0.85rem;
      padding: 0.35rem 0.9rem;
      border-radius: 999px;
      margin-bottom: 0.9rem;
    }
    .brand-title {
      font-family: 'Playfair Display', serif;
      font-size: 2.5rem;
      color: #c9186b;
      margin-bottom: 0.5rem;
    }
    .bio {
      max-width: 620px;
      margin: 0 auto 1.4rem;
      line-height: 1.65;
      font-size: 0.98rem;
      color: #631539;
    }
    .insta-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
      background: linear-gradient(90deg, #e11d74, #f472b6);
      color: #ffffff;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 0.85rem 1.65rem;
      border-radius: 999px;
      box-shadow: 0 8px 20px rgba(225, 29, 116, 0.3);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .insta-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 24px rgba(225, 29, 116, 0.38);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 1.5rem;
    }
    .card {
      background: rgba(255, 255, 255, 0.92);
      border-radius: 26px;
      padding: 1.8rem;
      border: 2px solid #ffffff;
      box-shadow: 0 12px 28px rgba(219, 39, 119, 0.14);
    }
    h2 {
      font-size: 1.3rem;
      color: #be185d;
      margin-bottom: 1.1rem;
    }
    .price-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 0.9rem 0;
      border-bottom: 1px dashed #f9a8d4;
      font-size: 0.95rem;
    }
    .price-row:last-child {
      border-bottom: none;
    }
    .price-pill {
      background: #fce7f3;
      color: #9d174d;
      font-weight: 700;
      padding: 0.35rem 0.85rem;
      border-radius: 999px;
      white-space: nowrap;
    }
    .form-group {
      margin-bottom: 1rem;
    }
    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 700;
      color: #831843;
      margin-bottom: 0.4rem;
    }
    input, select {
      width: 100%;
      padding: 0.8rem 1rem;
      border-radius: 16px;
      border: 2px solid #fbcfe8;
      background: #fff7fb;
      font-family: inherit;
      font-size: 0.94rem;
      color: #4a102b;
      outline: none;
    }
    input:focus, select:focus {
      border-color: #ec4899;
      background: #ffffff;
    }
    .submit-btn {
      width: 100%;
      padding: 0.95rem;
      border: none;
      border-radius: 999px;
      background: linear-gradient(90deg, #db2777, #f472b6);
      color: #ffffff;
      font-family: inherit;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 8px 20px rgba(219, 39, 119, 0.3);
      transition: transform 0.15s ease;
    }
    .submit-btn:hover {
      transform: translateY(-2px);
    }
    #status-msg {
      margin-top: 1rem;
      padding: 0.85rem 1rem;
      border-radius: 16px;
      background: #fce7f3;
      color: #9d174d;
      font-weight: 700;
      font-size: 0.9rem;
      display: none;
      text-align: center;
    }
    footer {
      text-align: center;
      margin-top: 1.8rem;
      font-size: 0.85rem;
      font-weight: 700;
      color: #831843;
    }
  </style>
</head>
<body>

<div class="container">
  <header>
    <div class="location-tag">Требухів • Сертифікований майстер</div>
    <h1 class="brand-title">Катерина • Манікюр</h1>
    <p class="bio">
      Привіт! Мене звати Катерина, мені 15 років, і я займаюся манікюром уже 4 роки.
      Сертифікований майстер — працюю акуратно, стерильно та з увагою до кожної деталі.
    </p>
    <a class="insta-btn" href="https://www.instagram.com/trebukhiv_nails/" target="_blank" rel="noopener noreferrer">
      Перейти в Instagram @trebukhiv_nails
    </a>
  </header>

  <div class="grid">
    <div class="card">
      <h2>Прайс-лист</h2>
      <div class="price-row">
        <span>Комплекс (зняття + чистка + гель-лак)</span>
        <span class="price-pill">500 ₴</span>
      </div>
      <div class="price-row">
        <span>Укріплення гелем / полігелем</span>
        <span class="price-pill">600 ₴</span>
      </div>
      <div class="price-row">
        <span>Нарощування нігтів (довжина 1–3)</span>
        <span class="price-pill">700 ₴</span>
      </div>
      <div class="price-row">
        <span>Дизайн</span>
        <span class="price-pill">+100 ₴</span>
      </div>
      <div class="price-row">
        <span>Комбінований манікюр без покриття</span>
        <span class="price-pill">300 ₴</span>
      </div>
    </div>

    <div class="card">
      <h2>Онлайн-запис</h2>
      <form id="booking-form">
        <div class="form-group">
          <label for="name">Твоє ім'я</label>
          <input type="text" id="name" placeholder="Наприклад, Софія" required>
        </div>
        <div class="form-group">
          <label for="contact">Телефон або Instagram</label>
          <input type="text" id="contact" placeholder="@username або +380..." required>
        </div>
        <div class="form-group">
          <label for="service">Послуга</label>
          <select id="service">
            <option value="Комплекс (зняття + чистка + гель-лак) — 500 ₴">Комплекс: зняття + чистка + гель-лак (500 ₴)</option>
            <option value="Укріплення гелем / полігелем — 600 ₴">Укріплення гелем / полігелем (600 ₴)</option>
            <option value="Нарощування нігтів (довжина 1–3) — 700 ₴">Нарощування нігтів, довжина 1–3 (700 ₴)</option>
            <option value="Комбінований манікюр без покриття — 300 ₴">Комбінований манікюр без покриття (300 ₴)</option>
          </select>
        </div>
        <div class="form-group">
          <label for="design">Додати дизайн (+100 ₴)?</label>
          <select id="design">
            <option value="Без дизайну">Без дизайну</option>
            <option value="Так, з дизайном (+100 ₴)">Так, з дизайном (+100 ₴)</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date">Бажаний день та час</label>
          <input type="text" id="date" placeholder="Наприклад, Субота о 14:00" required>
        </div>
        <button type="submit" class="submit-btn">Надіслати запис</button>
      </form>
      <div id="status-msg"></div>
    </div>
  </div>

  <footer>
    Катерина • Требухів • <a href="https://www.instagram.com/trebukhiv_nails/" target="_blank" rel="noopener noreferrer" style="color:#be185d;">@trebukhiv_nails</a>
  </footer>
</div>

<script>
  document.getElementById("booking-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const payload = {
      name: document.getElementById("name").value,
      contact: document.getElementById("contact").value,
      service: document.getElementById("service").value,
      design: document.getElementById("design").value,
      date: document.getElementById("date").value
    };

    const res = await fetch("/api/book", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    const msgBox = document.getElementById("status-msg");
    msgBox.style.display = "block";
    msgBox.textContent = data.message;
    document.getElementById("booking-form").reset();
  });
</script>

</body>
</html>
"""


class KaterynaNailsHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    clean_path = unquote(self.path.split("?", 1)[0])

    if clean_path == "/":
      body = HTML_PAGE.encode("utf-8")
      self.send_response(200)
      self.send_header("Content-Type", "text/html; charset=utf-8")
      self.send_header("Content-Length", str(len(body)))
      self.end_headers()
      self.wfile.write(body)
    elif clean_path == "/api/bookings":
      body = json.dumps(BOOKINGS, ensure_ascii=False, indent=2).encode("utf-8")
      self.send_response(200)
      self.send_header("Content-Type", "application/json; charset=utf-8")
      self.send_header("Content-Length", str(len(body)))
      self.end_headers()
      self.wfile.write(body)
    else:
      self.send_response(404)
      self.end_headers()

  def do_POST(self):
    if self.path == "/api/book":
      length = int(self.headers.get("Content-Length", 0))
      raw = self.rfile.read(length) if length > 0 else b"{}"
      data = json.loads(raw.decode("utf-8"))
      BOOKINGS.append(data)

      print(
          f"Новий запис: {data['name']} | {data['service']} | {data['design']} | {data['date']} | {data['contact']}"
      )

      resp_text = (
          f"Дякуємо, {data['name']}! Заявку на «{data['service']}» "
          f"({data['design']}, {data['date']}) прийнято."
      )
      resp = json.dumps({"ok": True, "message": resp_text}, ensure_ascii=False).encode("utf-8")
      self.send_response(200)
      self.send_header("Content-Type", "application/json; charset=utf-8")
      self.send_header("Content-Length", str(len(resp)))
      self.end_headers()
      self.wfile.write(resp)

  def log_message(self, format, *args):
    pass


if __name__ == "__main__":
  server = ThreadingHTTPServer(("127.0.0.1", 8000), KaterynaNailsHandler)
  print("Сайт запущено: http://127.0.0.1:8000")
  try:
    <!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Катерина • Манікюр Требухів (@trebukhiv_nails)</title>
  <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600;700&family=Playfair+Display:ital,wght@0,600;1,500&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Comfortaa', sans-serif;
      background: linear-gradient(145deg, #ffe4ef 0%, #ffd1e6 45%, #ffb6d9 100%);
      min-height: 100vh;
      color: #4a102b;
      padding: 2rem 1rem 3rem;
    }
    .container { max-width: 880px; margin: 0 auto; }
    header {
      text-align: center;
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(12px);
      padding: 2.3rem 1.5rem;
      border-radius: 28px;
      border: 2px solid #ffffff;
      box-shadow: 0 14px 32px rgba(219, 39, 119, 0.18);
      margin-bottom: 1.8rem;
    }
    .location-tag {
      display: inline-block;
      background: #fce7f3;
      color: #9d174d;
      font-weight: 700;
      font-size: 0.85rem;
      padding: 0.35rem 0.9rem;
      border-radius: 999px;
      margin-bottom: 0.9rem;
    }
    .brand-title {
      font-family: 'Playfair Display', serif;
      font-size: 2.5rem;
      color: #c9186b;
      margin-bottom: 0.5rem;
    }
    .bio {
      max-width: 620px;
      margin: 0 auto 1.4rem;
      line-height: 1.65;
      font-size: 0.98rem;
      color: #631539;
    }
    .insta-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
      background: linear-gradient(90deg, #e11d74, #f472b6);
      color: #ffffff;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 0.85rem 1.65rem;
      border-radius: 999px;
      box-shadow: 0 8px 20px rgba(225, 29, 116, 0.3);
      transition: transform 0.15s ease;
    }
    .insta-btn:hover { transform: translateY(-2px); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
    }
    .card {
      background: rgba(255, 255, 255, 0.92);
      border-radius: 26px;
      padding: 1.8rem;
      border: 2px solid #ffffff;
      box-shadow: 0 12px 28px rgba(219, 39, 119, 0.14);
    }
    h2 { font-size: 1.3rem; color: #be185d; margin-bottom: 1.1rem; }
    .price-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 0.9rem 0;
      border-bottom: 1px dashed #f9a8d4;
      font-size: 0.95rem;
    }
    .price-row:last-child { border-bottom: none; }
    .price-pill {
      background: #fce7f3;
      color: #9d174d;
      font-weight: 700;
      padding: 0.35rem 0.85rem;
      border-radius: 999px;
      white-space: nowrap;
    }
    .form-group { margin-bottom: 1rem; }
    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 700;
      color: #831843;
      margin-bottom: 0.4rem;
    }
    input, select {
      width: 100%;
      padding: 0.8rem 1rem;
      border-radius: 16px;
      border: 2px solid #fbcfe8;
      background: #fff7fb;
      font-family: inherit;
      font-size: 0.94rem;
      color: #4a102b;
      outline: none;
    }
    input:focus, select:focus { border-color: #ec4899; background: #ffffff; }
    .submit-btn {
      width: 100%;
      padding: 0.95rem;
      border: none;
      border-radius: 999px;
      background: linear-gradient(90deg, #db2777, #f472b6);
      color: #ffffff;
      font-family: inherit;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 8px 20px rgba(219, 39, 119, 0.3);
    }
    #status-msg {
      margin-top: 1rem;
      padding: 0.85rem 1rem;
      border-radius: 16px;
      background: #fce7f3;
      color: #9d174d;
      font-weight: 700;
      font-size: 0.9rem;
      display: none;
      text-align: center;
    }
    footer {
      text-align: center;
      margin-top: 1.8rem;
      font-size: 0.85rem;
      font-weight: 700;
      color: #831843;
    }
  </style>
</head>
<body>

<div class="container">
  <header>
    <div class="location-tag">Требухів • Сертифікований майстер</div>
    <h1 class="brand-title">Катерина • Манікюр</h1>
    <p class="bio">
      Привіт! Мене звати Катерина, мені 15 років, і я займаюся манікюром уже 4 роки.
      Сертифікований майстер — працюю акуратно, стерильно та з увагою до кожної деталі.
    </p>
    <a class="insta-btn" href="https://www.instagram.com/trebukhiv_nails/" target="_blank" rel="noopener noreferrer">
      Перейти в Instagram @trebukhiv_nails
    </a>
  </header>

  <div class="grid">
    <div class="card">
      <h2>Прайс-лист</h2>
      <div class="price-row">
        <span>Комплекс (зняття + чистка + гель-лак)</span>
        <span class="price-pill">500 ₴</span>
      </div>
      <div class="price-row">
        <span>Укріплення гелем / полігелем</span>
        <span class="price-pill">600 ₴</span>
      </div>
      <div class="price-row">
        <span>Нарощування нігтів (довжина 1–3)</span>
        <span class="price-pill">700 ₴</span>
      </div>
      <div class="price-row">
        <span>Дизайн</span>
        <span class="price-pill">+100 ₴</span>
      </div>
      <div class="price-row">
        <span>Комбінований манікюр без покриття</span>
        <span class="price-pill">300 ₴</span>
      </div>
    </div>

    <div class="card">
      <h2>Онлайн-запис</h2>
      <form id="booking-form" action="https://formspree.io/f/xaeobvww" method="POST">
        <div class="form-group">
          <label for="name">Твоє ім'я</label>
          <input type="text" id="name" name="Ім'я" placeholder="Наприклад, Софія" required>
        </div>
        <div class="form-group">
          <label for="contact">Телефон або Instagram</label>
          <input type="text" id="contact" name="Контакт" placeholder="@username або +380..." required>
        </div>
        <div class="form-group">
          <label for="service">Послуга</label>
          <select id="service" name="Послуга">
            <option value="Комплекс (зняття + чистка + гель-лак) — 500 ₴">Комплекс: зняття + чистка + гель-лак (500 ₴)</option>
            <option value="Укріплення гелем / полігелем — 600 ₴">Укріплення гелем / полігелем (600 ₴)</option>
            <option value="Нарощування нігтів (довжина 1–3) — 700 ₴">Нарощування нігтів, довжина 1–3 (700 ₴)</option>
            <option value="Комбінований манікюр без покриття — 300 ₴">Комбінований манікюр без покриття (300 ₴)</option>
          </select>
        </div>
        <div class="form-group">
          <label for="design">Додати дизайн (+100 ₴)?</label>
          <select id="design" name="Дизайн">
            <option value="Без дизайну">Без дизайну</option>
            <option value="Так, з дизайном (+100 ₴)">Так, з дизайном (+100 ₴)</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date">Бажаний день та час</label>
          <input type="text" id="date" name="Дата та час" placeholder="Наприклад, Субота о 14:00" required>
        </div>
        <button type="submit" class="submit-btn">Надіслати запис</button>
      </form>
      <div id="status-msg"></div>
    </div>
  </div>

  <footer>
    Катерина • Требухів • <a href="https://www.instagram.com/trebukhiv_nails/" target="_blank" rel="noopener noreferrer" style="color:#be185d;">@trebukhiv_nails</a>
  </footer>
</div>

<script>
  const form = document.getElementById("booking-form");
  const msgBox = document.getElementById("status-msg");

  form.addEventListener("submit", async function(e) {
    e.preventDefault();
    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { "Accept": "application/json" }
    });

    msgBox.style.display = "block";
    if (response.ok) {
      msgBox.textContent = "Дякуємо! Заявку надіслано Катерині, скоро зв'яжемося з тобою.";
      form.reset();
    } else {
      msgBox.textContent = "Виникла помилка під час відправки. Спробуй ще раз або напиши в Instagram.";
    }
  });
</script>

</body>
</html>
    server.serve_forever()
  except KeyboardInterrupt:
    print("\nСервер зупинено.")
    server.server_close()
