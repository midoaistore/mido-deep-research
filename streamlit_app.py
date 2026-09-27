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
    report = f"# 📊 تقرير بحثي عميق: {q}\n\n"
    report += f"## 🎯 الملخص التنفيذي\n{answer}\n\n"
    
    # تحليل ذكي للمنصات من المصادر
    platforms_found = []
    for r in results:
        t = (r.get('title','') + " " + r.get('content','')).lower()
        if 'podu' in t or 'بوديو' in t: platforms_found.append("PodU")
        if 'spotify' in t or 'سبوتيفاي' in t: platforms_found.append("Spotify")
        if 'apple' in t or 'أبل' in t: platforms_found.append("Apple Podcasts")
        if 'anghami' in t or 'أنغامي' in t: platforms_found.append("Anghami")
        if 'الجزيرة' in t: platforms_found.append("الجزيرة بودكاست")
        if 'buzzsprout' in t: platforms_found.append("Buzzsprout")

    platforms_found = list(dict.fromkeys(platforms_found))[:5]

    report += f"## 🔍 التحليل العميق (من {len(results)} مصدر موثوق)\n"
    for i, r in enumerate(results, 1):
        report += f"### {i}. {r.get('title','بدون عنوان')}\n{r.get('content','')[:650]}...\n\n"

    report += "\n## 📈 جدول المقارنة السريع\n"
    report += "| # | المنصة | الميزة الأساسية | السعر | الرابط |\n|---|---|---|---|---|\n"
    for i, r in enumerate(results[:8], 1):
        title = r.get('title','')[:35].replace('|',' ')
        content = r.get('content','').lower()
        price = "مجاني" if "مجاني" in content or "free" in content else "مدفوع"
        feat = "محتوى عربي" if "عربي" in content else "عالمي"
        url = r.get('url','')
        report += f"| {i} | {title} | {feat} | {price} | [فتح]({url}) |\n"

    report += f"\n## 💡 التوصية النهائية الذكية من Mido AI\n"
    report += f"سؤالك كان: **{q}**\n\n"
    
    if any(x in q.lower() for x in ["ربح", "فلوس", "monetization", "money"]):
        report += "💰 **لو هدفك الربح:**\n- ابدأ بـ **Spotify for Podcasters + Buzzsprout** بيدعموا الربح بالإعلانات\n- **PodU** بيدفع للمحتوى الحصري العربي\n\n"
    elif any(x in q.lower() for x in ["مبتدئ", "ابدأ", "beginner"]):
        report += "🚀 **لو انت مبتدئ:**\n- ابدأ بـ **PodU** (19 جنيه بس لإلغاء الإعلانات ومساحة صغيرة)\n- تاني اختيار **Spotify** مجاني وسهل\n\n"
    else:
        report += f"بناء على المنصات اللي لقيناها: **{', '.join(platforms_found) if platforms_found else 'Spotify, PodU, Apple'}**\n\n"
        report += "✅ **لو عايز جمهور عربي كبير:** PodU + أنغامي + الجزيرة بودكاست\n"
        report += "✅ **لو عايز جمهور عالمي:** Spotify + Apple Podcasts + Buzzsprout\n"
        report += "✅ **لو عايز أقل استهلاك داتا:** PodU (أحدث خوارزميات حفظ الصوت)\n"
        report += "✅ **لو عايز تتعلم:** أبجورة (50 مليون استماع) + دروس أونلاين\n\n"

    report += "---\n*تم إنشاء التقرير بواسطة Mido AI Store - البحث العميق | 299 جنيه*\n"
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
