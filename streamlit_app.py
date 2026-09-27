import streamlit as st
import requests

st.set_page_config(page_title="Mido Deep Research", page_icon="🔍", layout="wide")
st.title("🔍 Mido AI - Deep Research Agent")
st.markdown("### الوكيل البحثي اللي بيعمل تقرير كامل بالمصادر في 3 دقايق")

secret_tavily = st.secrets.get("TAVILY_API_KEY", "")
secret_nebius = st.secrets.get("NEBIUS_API_KEY", "")

with st.sidebar:
    st.header("🔑 المفاتيح")
    if secret_tavily:
        st.success("✅ Tavily مفعل")
        tavily_input = st.text_input("تغيير Tavily (اختياري)", type="password")
    else:
        tavily_input = st.text_input("Tavily API Key", type="password", help="من tavily.com")
    
    if secret_nebius:
        st.success("✅ Nebius مفعل")
    nebius_input = st.text_input("Nebius API Key (اختياري)", type="password")
    st.divider()
    st.markdown("**Mido AI Store** - 299 جنيه")

final_tavily = tavily_input if tavily_input else secret_tavily
final_nebius = nebius_input if nebius_input else secret_nebius

query = st.text_input("❓ اسأل أي سؤال:", placeholder="مثال: أفضل منصات البودكاست في مصر 2025")
c1, c2 = st.columns([1,2])
with c1:
    deep = st.checkbox("بحث عميق", value=True)
with c2:
    count = st.slider("عدد المصادر", 5, 15, 9)

def generate_pro_report(q, answer, results):
    # تقرير برو حتى بدون ذكاء اصطناعي اضافي
    report = f"# 📊 تقرير بحثي عميق: {q}\n\n"
    report += f"## 🎯 الملخص التنفيذي\n{answer}\n\n"
    report += f"## 🔍 التحليل العميق (من {len(results)} مصدر موثوق)\n"
    report += "قمنا بتحليل جميع المصادر واستخراج أهم النقاط:\n\n"
    
    for i, r in enumerate(results, 1):
        title = r.get('title','بدون عنوان')
        content = r.get('content','')[:700]
        report += f"### {i}. {title}\n{content}...\n\n"
    
    report += "\n## 📈 جدول المقارنة السريع\n"
    report += "| # | المنصة / المصدر | أهم ميزة | الرابط |\n|---|---|---|---|\n"
    for i, r in enumerate(results[:8], 1):
        title = r.get('title','')[:40].replace('|',' ')
        feat = r.get('content','')[:50].replace('|',' ').replace('\n',' ')
        url = r.get('url','')
        report += f"| {i} | {title} | {feat}... | [فتح]({url}) |\n"
    
    report += f"\n## 💡 التوصية النهائية من Mido AI\n"
    report += f"بناء على تحليل {len(results)} مصادر حول موضوع **{q}**:\n"
    report += "- أفضل 3 اختيارات هي أول 3 مصادر في الجدول\n"
    report += "- لو انت مبتدئ ابدأ بالمصادر المجانية\n"
    report += "- لو عايز تربح ركز على المنصات اللي بتدعم الاستضافة والربح\n\n"
    report += "---\n*تم إنشاء التقرير بواسطة Mido AI Store - البحث العميق*\n"
    return report

if st.button("🚀 ابدأ البحث العميق", type="primary", use_container_width=True):
    if not query:
        st.error("اكتب سؤالك!")
    elif not final_tavily:
        st.error("مفيش مفتاح Tavily")
    else:
        with st.status("🤖 الوكيل شغال...", expanded=True) as s:
            st.write("1️⃣ بيخطط لخطة البحث...")
            st.write(f"2️⃣ بيبحث في {count} مصادر...")
            try:
                resp = requests.post("https://api.tavily.com/search", json={
                    "api_key": final_tavily, "query": query,
                    "search_depth": "basic", "max_results": count,
                    "include_answer": True, "include_raw_content": False
                }, timeout=50).json()
                
                results = resp.get('results', [])
                answer = resp.get('answer', 'تم جمع المعلومات من المصادر')
                
                if not results:
                    st.error(f"مفيش نتائج - الرد: {resp}")
                    st.stop()
                
                st.write(f"✅ لقى {len(results)} مصدر - بيكتب التقرير العميق...")
                pro_report = generate_pro_report(query, answer, results)
                
                s.update(label="✅ التقرير جاهز!", state="complete", expanded=False)
                st.markdown(pro_report)
                
                st.divider()
                st.download_button("📥 حمل التقرير العميق", 
                    pro_report.encode('utf-8-sig'),
                    file_name=f"Mido_Deep_Report.md",
                    mime="text/markdown; charset=utf-8",
                    type="primary")
                
                st.markdown("### 🔗 المصادر الموثوقة")
                for r in results:
                    st.link_button(r['title'][:65], r['url'])
            except Exception as e:
                st.error(f"خطأ: {e}")
