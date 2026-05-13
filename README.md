# 🔐 Quantum Hacker Detection System (BB84 Protocol)

## 📌 Overview

This project demonstrates a **Quantum Cryptography-based Hacker Detection System** using the **BB84 protocol**.

It simulates how secure communication works in quantum systems and how an eavesdropper (hacker) can be detected using **QBER (Quantum Bit Error Rate)**.

---

## 🚀 Features

* ✅ BB84 Protocol Simulation
* ✅ Hacker Detection using QBER
* ✅ Interactive GUI (Tkinter)
* ✅ Matrix-style Cybersecurity UI
* ✅ Alarm alert on intrusion 🚨
* ✅ Graph visualization (QBER comparison)

---

## 🧠 Concept

In quantum communication:

* Data is sent using **qubits (photons)**
* Any interception **changes the quantum state**
* This introduces errors (QBER)
* If QBER > threshold → 🚨 Hacker detected

---

## 🖥️ Demo

### 🔹 Without Hacker

* QBER ≈ 0%
* Status: SECURE ✅

### 🔹 With Hacker

* QBER increases significantly
* Status: HACKER DETECTED 🚨
* Alarm sound triggered

---

## 🛠️ Tech Stack

* Python 🐍
* Tkinter (GUI)
* Matplotlib (Graph)
* Winsound (Alarm)

---

## 📂 Project Structure

```
quantum-project/
│── bb84_project.py        # Core BB84 simulation
│── gui_bb84.py            # GUI application
│── alarm.wav              # Alert sound
│── README.md              # Project documentation
```

---

## ▶️ How to Run

```bash
pip install matplotlib
python gui_bb84.py
```

---

## 📊 Output

* Real-time simulation of secure vs hacked communication
* Visual graph of QBER values
* Popup alerts + sound

---

## 🔬 Real World Application

This concept is used in:

* Quantum Key Distribution (QKD)
* Secure banking systems
* Military communication
* Future internet security

---

## 👨‍💻 Author

**Nishant Kumar**

---

## ⭐ Future Improvements

* Integration with Qiskit (real quantum simulation)
* Web-based dashboard
* Hardware implementation using optics

---

## 💡 Conclusion

This project shows how **quantum physics ensures security** and how any hacker attempt can be detected instantly.

---

⭐ If you like this project, give it a star and if you have any issues you can raise a issue!!!
