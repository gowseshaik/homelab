You'll need Node.js and a React environment to run this game. Here's the **complete setup guide**:

## 🚀 **Step-by-Step Setup:**

### **1. Install Node.js**

- Go to [nodejs.org](https://nodejs.org)
- Download and install **LTS version** (recommended)
- Verify installation: Open terminal/command prompt and type:

```bash
node --version
npm --version
```

### **2. Create React Project**

Choose one of these methods:

**Option A: Using Create React App (Easier)**

```bash
npx create-react-app codebot-game
cd codebot-game
```

**Option B: Using Vite (Faster)**

```bash
npm create vite@latest codebot-game -- --template react
cd codebot-game
npm install
```

### **3. Install Required Dependencies**

```bash
npm install lucide-react
```

### **4. Replace Default Code**

1. Open the project folder in your code editor
2. Find `src/App.js` (or `src/App.jsx`)
3. **Delete all content** in App.js
4. **Copy and paste** the entire CodeBot game code I provided
5. **Rename** `App.js` to `App.jsx` (or keep as `.tsx` if using TypeScript)

### **5. Update src/index.css (Optional)**

Replace content with:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}
```

### **6. Run the Game**

```bash
npm start
```

**Your game will open at:** `http://localhost:3000` 🎮

## 📁 **Final File Structure:**

```
codebot-game/
├── src/
│   ├── App.jsx (your game code here)
│   ├── index.js
│   └── index.css
├── public/
└── package.json
```

## 🛠️ **Troubleshooting:**

**If you get Tailwind CSS errors:**

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**If you prefer no setup:**

- Use **CodeSandbox** or **StackBlitz** online
- Just paste the code and it runs immediately!

## 🌐 **Alternative (No Installation):**

1. Go to [codesandbox.io](https://codesandbox.io)
2. Choose "React" template
3. Paste my code in `App.js`
4. Install `lucide-react` dependency
5. Play immediately! ✨
