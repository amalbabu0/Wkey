<p align="center">
  <img src="web/logo.svg" alt="weys logo" width="96" height="96">
</p>

<h1 align="center">weys</h1>

<p align="center"><strong>Speak to your phone, watch your computer type the code for you.</strong></p>

<p align="center">
  Developed by <strong><a href="https://amalbabu.xyz">Amal Babu</a></strong> &nbsp;·&nbsp;
</p>

---

weys is a small project that lets you describe what you want in plain words on your phone, and a tiny gadget then types the answer onto your computer — as if a real person were sitting at the keyboard typing it for you.

You don't need to know how to code to set this up. If you can plug in a USB cable, copy a file, and follow numbered steps, you can do this.

---

## What is this, really?

Imagine you want a computer program written. Normally you'd:
1. Open a website with an AI (like ChatGPT).
2. Type your question.
3. Copy the answer.
4. Switch to your code editor.
5. Paste it.

This project removes steps 3–5. You just tap a button on your phone, and the code appears on your PC screen automatically — letter by letter, like magic typing.

### How is the magic done?

There are **three players**:

| Player | What it is | What it does |
|---|---|---|
| **Your phone** | A web page open in your phone's browser | You type what you want here |
| **The AI** | A free online service like Google Gemini | Writes the code based on your request |
| **A tiny gadget (Pico W)** | A small electronic chip the size of a stick of gum | Pretends to be a keyboard plugged into your PC and types the code |

They talk to each other over your home Wi-Fi.

```
   YOU                    PHONE                AI ONLINE              PICO GADGET             YOUR PC
   ───                    ─────                ─────────              ───────────             ───────
"Write me a   ──▶  Sends to AI    ──▶   Returns code    ──▶   Pico types it   ──▶   Code appears
 program..."       over Wi-Fi              back               like a keyboard         on screen
```

---

## What's in this project

When you unzip or download this project, this is what you'll see:

```
wkey/
├── Main.py           ← the program for the Pico gadget
├── Readme.MD         ← this guide
└── web/              ← the phone app (4 files that work together)
    ├── Mobileapp.html
    ├── Styles.css
    ├── App.js
    └── logo.svg      ← the app icon
```

- **`Main.py`** goes onto the Pico gadget (Step 2 explains how).
- **The `web` folder** is the phone app. All four files inside must stay together.

---

## What you'll need

### One small gadget — the Raspberry Pi Pico W

This is the "magic typing" gadget. It's a small electronics board, about the size of half a credit card.

- **Cost:** roughly $6–$10 (around ₹500–₹800)
- **Where to buy:** Amazon, Robu.in, electronics shops — search for *"Raspberry Pi Pico W"*
- **Important:** Make sure it's the **"W" version** (the W means it has Wi-Fi). A plain "Pico" without the W will not work.
- **Also works:** "Pico 2 W" (a newer version)

### A USB cable
A regular **micro-USB cable** — the same kind older phones, e-readers, or game controllers used. One end goes into the Pico W, the other end into your PC.

### A phone
Any phone — iPhone or Android — that can open a web browser (Chrome, Safari, etc.).

### A PC or laptop
Any computer — Windows, Mac, or Linux. You don't need to install anything special on it. The Pico will appear to your PC as a normal keyboard.

### Home Wi-Fi
Your phone and the Pico must be on the **same Wi-Fi network** so they can talk to each other.

> ⚠️ Pico W only works with **2.4 GHz Wi-Fi** (the older, more common kind). Most home routers broadcast both 2.4 GHz and 5 GHz — that's fine, just make sure you connect to the 2.4 GHz one.

### A free AI account (5-minute signup)
You'll need a free "API key" from one of these — think of an API key as a password that lets the app talk to the AI:

| AI Service | Free? | Sign up at |
|---|---|---|
| **Google Gemini** ⭐ recommended | Yes — generous free use, no credit card | aistudio.google.com |
| **Groq** | Yes — very fast, no credit card | console.groq.com |
| **OpenRouter** | Yes — many free models | openrouter.ai |

Pick **Google Gemini** if you're not sure — it's the easiest.

---

## What you'll do (the big picture)

You'll only set this up **once**. After that, using it takes seconds.

1. **Prepare the gadget** — load some software onto the Pico W (a one-time setup).
2. **Tell the gadget your Wi-Fi name and password** — so it can connect.
3. **Open the phone app** — a single web page you'll open in your phone's browser.
4. **Paste your AI key into the app** — so it can talk to the AI.
5. **Use it!** — type a request, tap a button, watch your PC type the answer.

Total setup time: about **20–30 minutes** the first time. After that, every use takes about **10 seconds**.

---

## Step-by-step setup

### Step 1 — Prepare the Pico W gadget (one-time)

The Pico W comes blank. We need to put two things on it:
- **A small program file** that makes it act like a keyboard and connect to Wi-Fi.
- **A helper library** (like a toolbox the program uses).

**1a. Put the Pico into "setup mode":**
- Find the small button on the Pico labeled `BOOTSEL`.
- **Press and hold it.**
- While still holding the button, plug the USB cable into your PC.
- After 2 seconds, let go of the button.
- A new drive appears on your PC, called `RPI-RP2` — like plugging in a USB stick.

**1b. Install the "operating system" for the Pico:**
- On your PC, open this link in a browser: https://circuitpython.org/board/raspberry_pi_pico_w/
- Download the file ending in `.uf2` (it's about 1 MB).
- **Drag that file onto the `RPI-RP2` drive** — just like copying a file to a USB stick.
- The drive disappears for a moment, then comes back with a new name: `CIRCUITPY`. Done.

> 💡 *What just happened?* You installed CircuitPython — a simple programming language environment — onto the Pico. Think of it like installing Windows on a brand-new PC.

**1c. Add the keyboard "toolbox":**
- Download the toolbox bundle from: https://circuitpython.org/libraries
- Unzip the downloaded file (right-click → Extract All on Windows).
- Inside, find a folder called `adafruit_hid`.
- On the `CIRCUITPY` drive, there should be a folder called `lib`. If not, create one.
- **Copy the entire `adafruit_hid` folder into `lib`.**

> 💡 *What just happened?* You added the "pretend to be a keyboard" toolbox. Without this, the Pico wouldn't know how to type.

---

### Step 2 — Tell the Pico your Wi-Fi info

**2a. Open the `main.py` file** that came with this project. You can open it with **Notepad** (Windows) or **TextEdit** (Mac) — it's just a text file.

**2b. Find these two lines near the top:**
```
WIFI_SSID     = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

**2c. Replace them with your real Wi-Fi name and password** — keep the quotation marks:
```
WIFI_SSID     = "MyHomeWiFi"
WIFI_PASSWORD = "supersecret123"
```

**2d. Save the file.**

**2e. Copy `main.py` onto the `CIRCUITPY` drive** — just drag and drop it into the top level of the drive (not inside any folder).

That's it. The Pico is now programmed.

---

### Step 3 — Find the Pico's address on your Wi-Fi

Every device on Wi-Fi has a numeric address called an **IP address** — like a house number on a street. The phone app needs to know the Pico's address to send it messages.

**3a. Install Thonny** — a free program that lets us peek at what the Pico is doing:
- Download from: https://thonny.org
- Install it like any other program.

**3b. Open Thonny.** At the **bottom-right corner**, click and choose **"MicroPython (CircuitPython - generic)"** or the option that mentions the Pico.

**3c. Look at the bottom panel** — you'll see text appearing. Press the small red **Stop** button, then the green **Run** button (or just unplug and replug the Pico).

You should see something like this:
```
========================================
  weys — Pico W
========================================
Keyboard HID ready
Connecting to WiFi: MyHomeWiFi
Connected! IP address: 192.168.1.42

>>> In the mobile app, set Pico IP to: 192.168.1.42 <<<
```

**3d. Write down that IP address** (in this example: `192.168.1.42`). Yours will be different. You'll need it in a moment.

> ⚠️ **If it says "Connection failed"** — double-check your Wi-Fi name and password in `main.py`. Also make sure your Wi-Fi is **2.4 GHz**, not 5 GHz only.

---

### Step 4 — Open the phone app

The phone app lives in the `web` folder of this project. It's made of **four files that work together**:

| File | What it does |
|---|---|
| `Mobileapp.html` | The page itself — buttons, boxes, layout |
| `Styles.css` | The colors, fonts, and visual design |
| `App.js` | The brain — talks to the AI and the Pico |
| `logo.svg` | The app icon shown in the header and browser tab |

> ⚠️ **All four files must stay together in the same folder.** If you only open `Mobileapp.html` by itself, it will look broken and won't work.

You have two ways to use the app — pick whichever fits.

#### Recommended — host it from your PC over Wi-Fi
This keeps everything on your home network, which works best with the Pico.

On your **PC**, open a command window:
- **Windows:** Press the Windows key, type `powershell`, press Enter.
- **Mac:** Open the Terminal app.

Then type these two commands (one at a time, press Enter after each):
```
cd "c:\Users\2457786\OneDrive - Cognizant\Desktop\wkey\web"
python -m http.server 8000
```

> 💡 The `cd` command moves into the `web` folder. The second command starts a tiny website on your PC, on port `8000`.

Find your PC's IP address:
- **Windows:** in PowerShell, type `ipconfig` and look for "IPv4 Address" (e.g. `192.168.1.50`).
- **Mac:** System Settings → Wi-Fi → Details → IP address.

Then on your **phone's browser**, type:
```
http://YOUR-PC-IP:8000/Mobileapp.html
```
For example: `http://192.168.1.50:8000/Mobileapp.html`

Keep the PowerShell/Terminal window open while you use the app — closing it shuts off the mini-website.

#### Easier but with a catch — drag-and-drop to Netlify
1. On your PC, open https://app.netlify.com/drop in a browser.
2. Drag the entire `web` folder (with all three files inside) onto the page.
3. Netlify gives you a link like `https://random-name.netlify.app`.
4. On your phone, open `https://random-name.netlify.app/Mobileapp.html`.

> ⚠️ **The catch:** Netlify uses secure (https) connections. Some phones block secure pages from talking to the Pico (which uses plain http). If you get "pico offline" errors, switch to the PC-hosted method above.

---

### Step 5 — Get your free AI key

We'll use **Google Gemini** because it's free and easy.

1. On your PC, open https://aistudio.google.com
2. Sign in with any Google account.
3. Click **"Get API key"** (top-left area).
4. Click **"Create API key"** → **"Create API key in new project"**.
5. A long string starting with `AIza...` appears. **Copy it.** This is your key.

> 🔒 **Treat this key like a password** — don't share it publicly. It links to your free Google account.

---

### Step 6 — Configure the phone app

On your phone, with the `Mobileapp.html` page open:

1. **Tap the "setup" pill** in the top-right corner — a settings panel opens.
2. **API Key** — paste the `AIza...` key you copied. The app automatically recognizes it as Gemini.
3. **Model** — leave the default value alone.
4. **Pico W IP Address** — type the IP address you wrote down in Step 3 (e.g. `192.168.1.42`).
5. **Typing delay** — leave at `50ms`. (If your PC seems to miss letters later, drag this slider higher — `80` or `100`.)
6. Tap **"Save & Connect"**.

The status pill at the top should turn **green** and say **"pico ready"**. 🎉

> ❌ If it says **"pico offline"**:
> - Make sure your phone is on the **same Wi-Fi** as the Pico.
> - Double-check the IP address.
> - Unplug and replug the Pico, wait 30 seconds, then try again.

---

### Step 7 — Use it!

You're done setting up. Here's how to use it every day:

1. **Plug the Pico** into any USB port on your PC. (It can be a USB charger too — it just needs power.)
2. **Open the phone app.**
3. **Pick a language** — tap COBOL, Java, Python, or whichever you want.
4. **Type your request** in the prompt box. Example: *"write a program that adds two numbers and shows the result"*
5. **Tap "Generate"** — the AI writes the code. It appears on your phone screen.
6. **On your PC**, click into wherever you want the code to appear — Notepad, your code editor, a terminal, etc. The cursor should be blinking in the right spot.
7. **Tap "⌨ Type it on PC"** on your phone.
8. **Watch your PC** — the code starts typing itself, letter by letter, into whatever window you clicked. 🪄

> ⏱️ You have **1.5 seconds** between tapping "Type it on PC" and the typing starting. Use that to click into your editor.

---

## What can it write?

The project is specifically tuned for two older programming languages still used in banks and large companies:

- **COBOL** ⭐ — a language from the 1960s, still running banks worldwide.
- **JCL** ⭐ — a job-control language used on IBM mainframes.

It also writes regular modern code: Java, Python, C++, JavaScript, Kotlin, Go, TypeScript, Rust.

---

## When something goes wrong

### "Pico offline" in the app
- Your phone and Pico must be on **the same Wi-Fi**.
- Check the IP address — re-read it from Thonny.
- Make sure `main.py` is in the **top level** of the CIRCUITPY drive, not inside a folder.
- Unplug Pico, wait 10 seconds, plug it back in.

### Wrong letters appear on the PC
- The Pico assumes a **US keyboard layout**. If your PC uses UK, French, German, etc., some symbols will be wrong.
- Increase the **typing delay** slider in settings — your PC may not be keeping up.

### AI returns an explanation instead of just code
- Switch the **Model** field in settings to `gemini-2.0-flash` (it follows rules better).
- Reword your request to be more specific.

### Wi-Fi won't connect at all
- Pico W only does **2.4 GHz** Wi-Fi. If your router only broadcasts 5 GHz, you'll need to enable 2.4 GHz in router settings (or ask whoever set up your router).
- Recheck the Wi-Fi name and password for typos in `main.py`. Capital letters matter.

### Typing seems too fast / too slow
- Open settings, drag the **Typing delay** slider:
  - **Faster:** `20–40ms` (works for simple editors like Notepad)
  - **Default:** `50ms`
  - **Slower / safer:** `80–100ms` (good for COBOL, mainframe terminals, or slow editors)

---

## Quick reference card

Once everything is set up, this is all you do:

```
1. Plug in Pico  ──▶  2. Open phone app  ──▶  3. Type request  ──▶  4. Tap Generate
                                                                              │
                                                                              ▼
                                          5. Click into PC editor  ──▶  6. Tap "Type it on PC"
                                                                              │
                                                                              ▼
                                                                       🎉 Code types itself!
```

---

## Glossary — terms explained

| Term | What it means in plain words |
|---|---|
| **Pico W** | A tiny electronics gadget the size of a stick of gum that we program to act like a keyboard. The "W" version has Wi-Fi built in. |
| **USB HID** | The technical term for "pretends to be a keyboard or mouse." HID stands for "Human Interface Device." |
| **CircuitPython** | A simplified programming language we put on the Pico — like an operating system for the gadget. |
| **Wi-Fi 2.4 GHz** | The older, more common type of home Wi-Fi. Most routers broadcast both 2.4 and 5 GHz; the Pico only understands 2.4. |
| **IP address** | A numeric "house number" like `192.168.1.42` that identifies a device on your Wi-Fi. |
| **API key** | A long secret password from an AI company that lets the phone app talk to the AI. |
| **API** | A way for two programs to talk to each other over the internet. |
| **AI model** | The specific "brain" doing the writing — e.g. `gemini-2.0-flash` is Google's fast model. |
| **localhost / 192.168.x.x** | Addresses that only work inside your own home Wi-Fi — not visible to the rest of the internet. |
| **Thonny** | A free program for your PC that lets you peek at what the Pico is doing. |
| **Serial monitor** | The bottom panel in Thonny where the Pico prints messages. |
| **`main.py`** | The name of the program file that the Pico automatically runs when it powers on. |
| **`CIRCUITPY`** | The name your PC gives the Pico when you plug it in — it looks like a USB stick. |
| **COBOL** | An old programming language from 1959, still running banking systems worldwide. |
| **JCL** | "Job Control Language" — a script language used on IBM mainframe computers. |
| **`http://`** | A way for the phone and Pico to send messages to each other over Wi-Fi. |
| **Markdown / code fences** | Formatting tricks AIs sometimes add (triple backticks). The app strips them out automatically. |

---

## Credits

<p align="left">
  <img src="web/logo.svg" alt="weys logo" width="48" height="48" align="left" style="margin-right: 12px;">
</p>

Designed and developed by **Amal Babu**.

- 🌐 Website: [amalbabu.xyz](https://amalbabu.xyz)
- 💻 GitHub: [@amalbabu0](https://github.com/amalbabu0)

If you build something cool with weys, I'd love to hear about it.

---

## License

MIT — free to use, modify, and share with anyone.
