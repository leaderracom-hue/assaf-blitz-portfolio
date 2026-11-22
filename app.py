"""Assaf Blitz: interactive portfolio. Seven AI products, from lead to meeting.

Same facts as Assaf-Blitz-Portfolio-EN.html; every number there is a measured pilot number. The "Try it" panels are
illustrations of each product's rules, computed in this page, not calls to the real systems.
"""
import html

import streamlit as st

st.set_page_config(page_title='Assaf Blitz · Portfolio', page_icon='◆', layout='wide', initial_sidebar_state='collapsed')

ACCENT, ACCENT_SOFT, INK, MUTED, LINE = '#0E5A6B', '#E2F0F3', '#12202B', '#55636F', '#DAE0E6'
OK, OK_SOFT, PART, PART_SOFT, BAD, BAD_SOFT = '#1C6B3C', '#E3F2E9', '#8A5A00', '#FBF0D9', '#9B2C2C', '#F9E5E5'

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');
.block-container {{ max-width: 1040px; padding-top: 2.4rem; padding-bottom: 3rem; }}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none; }}
.eyebrow {{ font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: .05em; color: {ACCENT}; }}
.hero h1 {{ font-size: clamp(32px, 5.4vw, 52px); line-height: 1.1; font-weight: 800; margin: 8px 0 12px; color: {INK}; }}
.lead {{ font-size: 18px; color: {MUTED}; max-width: 62ch; }}
.scope {{ font-size: 14px; color: {MUTED}; border-left: 3px solid {LINE}; padding-left: 12px; margin: 6px 0 4px; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 14px 0 6px; }}
.stat {{ background: #fff; border: 1px solid {LINE}; border-radius: 12px; padding: 12px 14px; }}
.stat .v {{ font-size: 26px; font-weight: 800; color: {INK}; line-height: 1.1; }}
.stat .l {{ font-size: 13px; color: {MUTED}; }}
.card-title {{ font-size: 19px; font-weight: 700; color: {INK}; line-height: 1.3; margin-bottom: 4px; }}
.card-text {{ font-size: 14.5px; color: {MUTED}; min-height: 66px; }}
.rank {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: {MUTED}; }}
.badge {{ display: inline-block; font-size: 12.5px; border-radius: 5px; padding: 2px 9px; margin: 6px 0 2px; }}
.badge.ok {{ background: {OK_SOFT}; color: {OK}; }}
.badge.part {{ background: {PART_SOFT}; color: {PART}; }}
.pain {{ background: {PART_SOFT}; color: {PART}; border-radius: 8px; padding: 8px 12px; font-size: 14.5px; }}
.h3 {{ font-size: 12.5px; font-weight: 600; letter-spacing: .07em; text-transform: uppercase; color: {ACCENT}; margin: 2px 0 4px; }}
.flow {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: stretch; margin: 6px 0 10px; }}
.node {{ flex: 1 1 120px; border: 1px solid {LINE}; background: #fff; border-radius: 9px; padding: 9px 11px; font-size: 14px; line-height: 1.35; color: {MUTED}; }}
.node b {{ display: block; font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 500; color: {ACCENT}; }}
.node.done {{ background: {ACCENT_SOFT}; color: {INK}; }}
.node.on {{ background: {ACCENT}; color: #fff; border-color: {ACCENT}; box-shadow: 0 2px 10px rgba(14,90,107,.25); }}
.node.on b {{ color: #cfe7ee; }}
.node.stop {{ background: {BAD_SOFT}; color: {BAD}; border-color: #ecc; }}
.node.skip {{ opacity: .38; }}
.detail {{ background: #fff; border: 1px solid {LINE}; border-left: 4px solid {ACCENT}; border-radius: 10px; padding: 12px 16px; font-size: 15px; }}
.chip {{ display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 12px; border: 1px solid {LINE}; border-radius: 4px; padding: 2px 8px; margin: 0 6px 6px 0; background: #fff; }}
.rule {{ font-size: 14.5px; color: {MUTED}; margin: 6px 0; }}
.rule b {{ color: {INK}; font-weight: 600; }}
.proof {{ font-size: 14.5px; color: {MUTED}; }}
.score {{ font-size: 44px; font-weight: 800; line-height: 1; color: {INK}; }}
.band {{ display: inline-block; font-weight: 700; font-size: 15px; border-radius: 6px; padding: 3px 12px; margin-left: 10px; vertical-align: 10px; }}
.note {{ font-size: 12.5px; color: {MUTED}; font-style: italic; }}
.bubble {{ max-width: 80%; border-radius: 14px; padding: 9px 13px; margin: 6px 0; font-size: 15px; }}
.bubble.lead {{ background: #fff; border: 1px solid {LINE}; margin-left: auto; }}
.bubble.agent {{ background: {ACCENT_SOFT}; }}
.bubble.person {{ background: {OK_SOFT}; }}
.who {{ font-size: 11.5px; color: {MUTED}; margin-bottom: 2px; }}
.bar {{ height: 22px; border-radius: 5px; display: inline-block; vertical-align: middle; }}
.footer {{ color: {MUTED}; font-size: 14px; border-top: 1px solid {LINE}; padding-top: 14px; margin-top: 28px; }}
div[data-testid="stButton"] button {{ border-radius: 8px; }}
</style>
""", unsafe_allow_html=True)


def esc(s):
    return html.escape(str(s))


# ---------- content (same facts as the HTML portfolio) ----------

PRODUCTS = [
    dict(
        id='icp', nav='ICP engine', title='ICP engine: finding and scoring cold leads',
        result='Describe the offer and the ideal customer in plain words, and get back a ranked list, with an explanation and an outreach strategy for every record.',
        problem='Bought lists aren\'t matched to a specific offer, and a "good lead" is a gut call. Nothing explains why to approach this particular person, or what to say.',
        solution='The system searches data sources by the ICP, scores each record by its fit to the offer and not just by job title, verifies contact details, and writes a short explanation and an outreach strategy for each record.',
        steps=[('Offer and ICP described in words', 'You write who you sell to and what you offer, in plain language. No filters to learn.'),
               ('Search across data sources', 'The engine looks for people and companies that match that description.'),
               ('Verify email and phone', 'Contact details are checked before anyone is contacted.'),
               ('Fit score on four dimensions', 'Offer fit 30, decision maker 25, contact details 20, intent 25: 100 points in total.'),
               ('Explanation and outreach strategy', 'A short reason for the score, and how to open the conversation with this person.'),
               ('Ranked list and export', 'Records sorted by score, ready to export.')],
        rules=[('The score', 'offer fit 30, decision maker 25, contact details 20, intent 25. Hot from 82, Warm from 62 to 81, Cold below 62.'),
               ('A self-built alternative to Clay', 'I built the sourcing, enrichment and scoring layer myself, on data sources, enrichment providers and n8n. It does what Clay usually does at this stage: search by ICP, enrichment across several providers ordered by cost, verification, and a score with an explanation.')],
        stack=['Next.js', 'Supabase', 'REST API', 'MCP', 'Explorium', 'Claude Haiku', 'MillionVerifier', 'Twilio Lookup', 'n8n', 'HeyReach'],
        status=('Tested live on 25 records', 'part'),
        proof='In the live test: 25 records, of which 8 Hot, 16 Warm and 1 Cold, with a mobile number found for 24. Estimated cost: $0.16 to $0.24 per record. I have since moved enrichment to Smartlead SmartProspect and LeadMagic.',
    ),
    dict(
        id='scorers', nav='Scorers', title='The Scorers: fit scoring by industry',
        result='A 0 to 100 score for every lead, with a reason, tuned to the industry the lead works in.',
        problem='One score for everyone fits no one. A lead in real estate, insurance, finance or an agency is judged by different signals, and without the reason, the sales team doesn\'t trust the score.',
        solution='Scorers calibrated for finance, agencies, insurance and real estate, plus a general score with a niche adjustment for an unfamiliar industry. Every score comes with a reason, and if the LLM fails, a deterministic score takes its place.',
        steps=[('Enriched lead', 'A lead arrives with its company and role details already filled in.'),
               ('Detect the industry', 'The lead\'s industry decides which scorer reads it.'),
               ('Pick the matching scorer', 'Finance, agencies, insurance or real estate; a general scorer with a niche adjustment for anything else.'),
               ('0 to 100 score with a reason', 'The reason travels with the score, so sales can see why.'),
               ('Hot, Warm or Cold', 'The score is turned into a band the team acts on.'),
               ('Outreach queue by score', 'Higher scores are contacted first.')],
        rules=[('Fallback', 'when the model doesn\'t respond or returns invalid output, a score is calculated with fixed rules, and the lead moves on through the process.')],
        stack=['Claude Haiku', 'Claude Code skills', 'n8n', 'Airtable', 'JSON'],
        status=('Built; Score Single Lead live in the pilot', 'ok'),
        proof='',
    ),
    dict(
        id='cycle', nav='Full lead cycle', title='The full lead cycle: intake, routing, enrichment and outreach',
        result='One pipeline from the first touch to a conversation: every lead gets the same treatment, and the sequence stops the moment there\'s a reply.',
        problem='Leads come from different sources and are handled in separate tools and by hand. Outreach on several channels without coordination annoys people, and cold email alone gets a low response.',
        solution='A lead comes in from any source, is routed by source, enriched and verified, scored, and contacted across channels in a sequence. A reply or a meeting stops the sequence on every channel, and the conversation passes to Daniel.',
        steps=[('Intake: form, Meta, chat, import', 'Every source lands in the same pipeline.'),
               ('Routing by source', 'Where the lead came from decides the first move.'),
               ('Enrichment and verification', 'Email first; a phone number is bought only after a company email is found.'),
               ('Score', 'The lead gets its fit score and band.'),
               ('Multichannel outreach in sequence', 'Email, WhatsApp, iMessage, SMS, RCS, voice and LinkedIn, one after another.'),
               ('Stop on reply or meeting', 'A reply or a booking stops the sequence on every channel at once.'),
               ('Handoff to Daniel', 'The conversation continues with the intake agent.')],
        rules=[('Channels', 'email, WhatsApp, iMessage, SMS, RCS, voice and LinkedIn.'),
               ('Cost rule', 'a phone number is bought only after a company email is found. A channel policy based on signal strength is planned and not built.')],
        stack=['n8n', 'Meta Lead Ads', 'Smartlead', 'SmartProspect', 'LeadMagic', 'MillionVerifier', 'Apify', 'WhatsApp templates', 'LoopMessage', 'Vapi', 'HeyReach', 'Airtable'],
        status=('Live in the pilot', 'ok'),
        proof='93% send completion. In a small pilot: a 5.9% reply rate across channels vs 0.62% on cold email.',
    ),
    dict(
        id='daniel', nav='Daniel', title='Daniel, a multichannel intake agent',
        result='A lead who reaches out gets an instant answer, is qualified and gets a meeting booked, or a person joins the conversation.',
        problem='A lead waiting for an answer goes cold. A human team isn\'t available at every hour, and every inbound inquiry needs qualifying before a salesperson spends time on it.',
        solution='An agent that answers on WhatsApp, iMessage and website chat, asks the qualifying questions, offers times and books a meeting. Anyone who asks for a person gets a person, in the same conversation, and the agent goes quiet.',
        steps=[('Inbound message', 'A lead writes on WhatsApp, iMessage or the website chat.'),
               ('Identify the entry point', 'Which door the lead came through changes the opening.'),
               ('Conversation engine with saved state', 'The conversation remembers where it stopped.'),
               ('Qualifying questions', 'The few answers a salesperson needs before a call.'),
               ('Meeting on the calendar, or handoff to a person', 'A time is booked, or a person takes over and the agent goes quiet.'),
               ('Record updated and alert sent', 'The CRM record is updated and the team is told.')],
        rules=[('Product decision', 'on WhatsApp the engine is deterministic, with fixed wording, so the agent\'s behavior is predictable and can be tested.')],
        stack=['n8n', 'WhatsApp Cloud API', 'LoopMessage', 'Claude Haiku 4.5', 'Airtable', 'Cal.com'],
        status=('Live in the pilot', 'ok'),
        proof='4,271 inbound runs in n8n. A 64-node workflow.',
    ),
    dict(
        id='meeting', nav='Meeting lifecycle', title='The meeting lifecycle',
        result='Fewer meetings that disappear after they\'re booked, and fewer leads stuck halfway through booking.',
        problem='A booked meeting doesn\'t guarantee the lead shows up. A lead who started booking and stopped gets forgotten, and the salesperson finds out too late.',
        solution='Every Cal.com event triggers a chain: a confirmation message, a request to confirm 24 hours before, and a follow-up with anyone who got stuck. If the lead doesn\'t confirm, a person gets an alert.',
        steps=[('Meeting booked in Cal.com', 'The booking event starts the chain.'),
               ('Confirmation message', 'The lead gets the details right away.'),
               ('Request to confirm 24 hours before', 'A day before, the lead is asked to confirm.'),
               ('Lead confirms, or doesn\'t', 'The answer decides the next step.'),
               ('Alert to a person if not confirmed', 'A person follows up. Nothing is cancelled automatically.'),
               ('Status updated', 'The meeting status in the CRM reflects what happened.')],
        rules=[('Safety limits', 'the system never cancels meetings automatically. In test environments, outbound sending is blocked by a fail-closed gate.')],
        stack=['n8n', 'Cal.com webhooks', 'WhatsApp Cloud API', 'LoopMessage', 'Airtable'],
        status=('Partly live, partly in staging', 'part'),
        proof='',
    ),
    dict(
        id='crm', nav='CRM connection', title='CRM connection layer',
        result='Leads and meetings reach the client\'s CRM with no duplicates, and with a record of every action.',
        problem='Every client has a different CRM with different fields. Without one layer that translates between them, every new client is a new integration project, and duplicates pollute the data.',
        solution='One layer with a template per destination, field mapping, duplicate detection, a readiness check before sending, and an audit log for every sync.',
        steps=[('Event: a lead or a meeting', 'Something happened that the client\'s CRM should know about.'),
               ('Readiness check', 'If the connection isn\'t ready, crm_hold stops the sync instead of failing silently.'),
               ('Field mapping by template', 'Each destination has its own template.'),
               ('Duplicate check', 'An existing record is updated, not created twice.'),
               ('Send to the CRM', 'The record goes to the client\'s system.'),
               ('Entry in the sync log', 'Every sync leaves an audit entry.')],
        rules=[('Templates', 'HubSpot, GoHighLevel, Airtable, Google Sheets, CSV and webhook. A crm_hold mechanism stops syncing while the connection isn\'t ready.')],
        stack=['Next.js', 'Vercel', 'Supabase / Postgres', 'Webhooks', 'REST'],
        status=('Tested live with a webhook', 'part'),
        proof='The other templates are built and passed the readiness checks, and have not yet been tested against real CRM accounts.',
    ),
    dict(
        id='proxy', nav='Caching proxy', title='Caching proxy for the LLM',
        result='Same agent, same quality, lower cost for every turn in the conversation.',
        problem='Daniel\'s prompt is about 10,000 tokens. The Anthropic node in n8n doesn\'t expose cache_control, so every turn in the conversation pays for the whole prompt again.',
        solution='A small proxy that adds cache_control to the fixed part of the prompt and forwards the request to Anthropic. In n8n, only the credential\'s Base URL changes.',
        steps=[('Anthropic node in n8n', 'The workflow calls the model as before.'),
               ('Proxy on Vercel', 'The credential\'s Base URL points to the proxy instead of Anthropic.'),
               ('Adds cache_control', 'The fixed part of the prompt is marked for caching.'),
               ('Anthropic API', 'Later turns read the fixed part from the cache.'),
               ('Response back to n8n', 'The workflow gets the same answer, at a lower cost.')],
        rules=[('Tuning', 'the TTL went down from one hour to 5 minutes. Only lmChatAnthropic nodes go through the proxy.')],
        stack=['Vercel serverless', 'Anthropic prompt caching', 'n8n credentials'],
        status=('Live', 'ok'),
        proof='About 5.2× lower cost on a sample 4-turn conversation. This measures one conversation, not an average across all traffic.',
    ),
    dict(
        id='jobs', bonus=True, nav='Job engine', title='Job engine: finding and judging the right roles',
        result='One keyword searches the Israeli job boards and over 200 company career pages. Every role is read in full, matched to the profile and ranked, so the day starts with a short list instead of a hundred tabs.',
        problem='Job boards repeat the same roles, and the real requirements sit in the text, not the title. A keyword search lets engineering roles in disguise through, and checking many sites by hand takes hours every day.',
        solution='One keyword is sent to LinkedIn, Drushim, AllJobs, JobMaster and over 200 company career pages. Free rules remove what cannot fit before any paid call. Each remaining role is read in full by two independent Claude reviews, with a third when they disagree. The result is a 0 to 100 match, an eligibility check, a verdict and the CV to attach. The final click on every application is mine.',
        steps=[('One keyword, many sources', 'A keyword is searched on LinkedIn, Drushim, AllJobs and JobMaster, and across over 200 company career pages built on Comeet, Greenhouse, Lever and Ashby. The Hebrew boards get the Hebrew term.'),
               ('Free rules first', 'Title rules, excluded industries, a location rule and roles already applied to are removed before any paid call.'),
               ('Read the full post', 'The whole description is read, not just the title. Required languages, degrees, years and domains all live in the text.'),
               ('Two independent reviews', 'Two separate Claude reviews list every stated requirement as must or nice, with a quote as evidence. If their scores differ by more than 10 points, a third review decides.'),
               ('Match, eligibility, verdict', 'A 0 to 100 match, an eligibility check, and a verdict: Apply now, Apply, Maybe or Skip. A role scoring under 40 is never shown.'),
               ('Short list with the right CV', 'Roles are sorted by match, each with a one-line reason and the CV to attach. A role I applied to or removed does not come back.')],
        rules=[('Free before paid', 'the career pages and Drushim are read at no cost, and every rule that can stop a role runs before any Claude call.'),
               ('Never applies by itself', 'the system finds, judges and prepares. The final click on every application is mine.'),
               ('Outreach', 'a contact finder and an email verifier are built. Every message needs my approval before it goes out, and the paid lookups are still being tested.')],
        stack=['Python', 'Streamlit', 'Node.js', 'Apify', 'Claude Haiku', 'Structured JSON outputs', 'GitHub API (private data repo)', 'SmartProspect', 'MillionVerifier'],
        status=('Live; outreach step in testing', 'part'),
        proof='In the first test on 138 saved roles, reading the full post instead of the title moved 26 of them by 25 points or more, and surfaced what a title cannot show: a required language, a required degree, a domain I have not worked in. A daily cap on searches and a running count of tokens and scraping spend keep the cost visible.',
    ),
]
BY_ID = {p['id']: p for p in PRODUCTS}
MAIN = [p for p in PRODUCTS if not p.get('bonus')]   # the seven lead-to-meeting products; the rest are bonus projects
PAINS = [('Hard to find the right leads', 'icp', 'ICP engine: a self-built alternative to Clay'),
         ('Leads wait and go cold', 'daniel', 'Daniel: instant intake'),
         ('Follow-up stops after one attempt', 'cycle', 'An outreach sequence that stops on reply'),
         ('No clear way to tell a good lead', 'scorers', 'Enrichment, score and explanation'),
         ('Meetings that don\'t happen', 'meeting', 'The meeting lifecycle'),
         ('Handoffs without context', 'crm', 'History, CRM and handoff to a person')]


# ---------- navigation (also kept in the URL, so a product can be linked directly) ----------

if 'page' not in st.session_state:
    st.session_state.page = st.query_params.get('p') if st.query_params.get('p') in BY_ID else 'home'


def go(page):
    st.session_state.page = page
    if page == 'home':
        st.query_params.clear()
    else:
        st.query_params['p'] = page


def flow_html(steps, active=None, states=None):
    """A row of steps. `active` is highlighted; `states` (optional) gives each step done/stop/skip."""
    out = []
    for i, (label, _) in enumerate(steps):
        cls = (states or {}).get(i, '')
        if i == active:
            cls = 'on'
        elif active is not None and i < active and not cls:
            cls = 'done'
        out.append(f'<div class="node {cls}"><b>{i + 1:02d}</b>{esc(label)}</div>')
    return '<div class="flow">' + ''.join(out) + '</div>'


def badge(status):
    text, kind = status
    return f'<span class="badge {kind}">{esc(text)}</span>'


# ---------- home ----------

def home():
    st.markdown("""
<div class="hero">
  <div class="eyebrow">ASSAF BLITZ · PRODUCT MANAGER &amp; AI BUILDER</div>
  <h1>Seven AI products, from lead to meeting</h1>
  <p class="lead">Systems I defined and built with Claude Code. Each product solves one business problem, with a clear process and a documented stack. Tap any product to see how it works, and try its rules yourself.</p>
</div>""", unsafe_allow_html=True)
    st.link_button('LinkedIn profile', 'https://www.linkedin.com/in/ablitz', icon=':material/open_in_new:')

    st.markdown("""
<div class="stats">
  <div class="stat"><div class="v">290</div><div class="l">n8n workflows built</div></div>
  <div class="stat"><div class="v">99.1%</div><div class="l">execution success</div></div>
  <div class="stat"><div class="v">4,271</div><div class="l">inbound agent runs</div></div>
  <div class="stat"><div class="v">38,000</div><div class="l">CRM records</div></div>
</div>
<p class="scope">The systems are production scale; the volume through them is pilot scale: about 25 live leads and 22 meetings. Numbers are marked as a small sample, not as a business result.</p>
""", unsafe_allow_html=True)

    st.subheader('Start from the pain')
    st.caption('Clients in real estate and lending had leads, and the leads weren\'t closing. Pick a pain to see what was built for it.')
    picked = st.pills('Pain', [p[0] for p in PAINS], key='pain', label_visibility='collapsed')
    if picked:
        _, pid, sol = next(p for p in PAINS if p[0] == picked)
        with st.container(border=True):
            c1, c2 = st.columns([3, 1], vertical_alignment='center')
            c1.markdown(f'<div class="pain">{esc(picked)}</div><div style="margin-top:8px;font-size:16px">→ <b>{esc(sol)}</b></div>'
                        f'<div class="card-text" style="min-height:0;margin-top:4px">{esc(BY_ID[pid]["result"])}</div>', unsafe_allow_html=True)
            c2.button('Open this product', key=f'pain_open_{pid}', type='primary', on_click=go, args=(pid,), width='stretch')

    st.subheader('The seven products')
    for row in range(0, len(MAIN), 3):
        cols = st.columns(3)
        for col, (n, p) in zip(cols, list(enumerate(MAIN))[row:row + 3]):
            with col.container(border=True):
                st.markdown(f'<div class="rank">{n + 1} of {len(MAIN)}</div><div class="card-title">{esc(p["title"])}</div>'
                            f'<div class="card-text">{esc(p["result"])}</div>{badge(p["status"])}', unsafe_allow_html=True)
                st.button('Explore →', key=f'open_{p["id"]}', on_click=go, args=(p['id'],), width='stretch')

    bonus = [p for p in PRODUCTS if p.get('bonus')]
    if bonus:
        st.subheader('Beyond lead to meeting')
        st.caption('The same way of building, pointed at my own job search.')
        for p in bonus:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1], vertical_alignment='center')
                c1.markdown(f'<div class="rank">Bonus project</div><div class="card-title">{esc(p["title"])}</div>'
                            f'<div class="card-text" style="min-height:0">{esc(p["result"])}</div>{badge(p["status"])}', unsafe_allow_html=True)
                c2.button('Explore →', key=f'open_{p["id"]}', on_click=go, args=(p['id'],), width='stretch')

    st.markdown('<div class="footer">Assaf Blitz · Tel Aviv · All products were designed and built with Claude Code.</div>', unsafe_allow_html=True)


# ---------- the "Try it" panels: each one plays the product's own rules ----------

def try_icp():
    st.markdown('Move the four dimensions and watch the score and the band change. The starting values are the made-up example from the portfolio.')
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        fit = st.slider('Offer fit', 0, 30, 27, key='icp_fit')
        dm = st.slider('Decision maker', 0, 25, 22, key='icp_dm')
        contact = st.slider('Contact details', 0, 20, 18, key='icp_contact')
        intent = st.slider('Intent', 0, 25, 19, key='icp_intent')
    total = fit + dm + contact + intent
    band, bg, fg = ('Hot', BAD_SOFT, BAD) if total >= 82 else ('Warm', PART_SOFT, PART) if total >= 62 else ('Cold', ACCENT_SOFT, ACCENT)
    with c2.container(border=True):
        st.markdown(f'<div class="h3">Head of Growth · Example company</div><span class="score">{total}</span>'
                    f'<span class="band" style="background:{bg};color:{fg}">{band}</span>'
                    f'<div class="rule">Hot from 82 · Warm 62–81 · Cold below 62</div>', unsafe_allow_html=True)
        if band == 'Hot':
            st.markdown('<div class="rule"><b>Outreach strategy:</b> open with the job ad they posted, offer a test on an old lead list, and suggest a 15-minute call.</div>', unsafe_allow_html=True)
        elif band == 'Warm':
            st.markdown('<div class="rule">Worth contacting, after the Hot records.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="rule">Kept on the list, not contacted first.</div>', unsafe_allow_html=True)
    st.markdown('<p class="note">A made-up example to illustrate the output. Not a real record.</p>', unsafe_allow_html=True)


def try_scorers():
    c1, c2 = st.columns(2)
    industry = c1.segmented_control('Lead\'s industry', ['Finance', 'Agency', 'Insurance', 'Real estate', 'Other'], default='Real estate', key='sc_ind')
    model = c2.segmented_control('The model…', ['answers', 'fails or returns invalid output'], default='answers', key='sc_model')
    industry = industry or 'Real estate'
    scorer = 'the general scorer, with a niche adjustment' if industry == 'Other' else f'the {industry.lower()} scorer'
    p = BY_ID['scorers']
    if model == 'fails or returns invalid output':
        st.markdown(flow_html(p['steps'], states={0: 'done', 1: 'done', 2: 'done', 3: 'stop', 4: 'done', 5: 'done'}), unsafe_allow_html=True)
        st.markdown(f'<div class="detail">The lead is read by <b>{esc(scorer)}</b>. The model didn\'t give a usable answer, so a '
                    '<b>score calculated with fixed rules</b> takes its place, and the lead still reaches the queue.</div>', unsafe_allow_html=True)
    else:
        st.markdown(flow_html(p['steps'], states={i: 'done' for i in range(6)}), unsafe_allow_html=True)
        st.markdown(f'<div class="detail">The lead is read by <b>{esc(scorer)}</b>, gets a 0 to 100 score with a written reason, '
                    'a Hot, Warm or Cold band, and its place in the outreach queue.</div>', unsafe_allow_html=True)


def try_cycle():
    c1, c2, c3 = st.columns(3)
    source = c1.selectbox('Where the lead came from', ['Form', 'Meta lead ad', 'Chat', 'Import'], key='cy_src')
    email = c2.segmented_control('Company email found?', ['Yes', 'No'], default='Yes', key='cy_email')
    outcome = c3.selectbox('What the lead does', ['Doesn\'t answer yet', 'Replies', 'Books a meeting'], key='cy_out')
    p = BY_ID['cycle']
    if outcome == 'Doesn\'t answer yet':
        states, active = {0: 'done', 1: 'done', 2: 'done', 3: 'done', 5: 'skip', 6: 'skip'}, 4
        text = 'The sequence keeps going, one channel after another.'
    else:
        states, active = {i: 'done' for i in range(5)}, 5
        states[6] = 'done'
        text = ('The reply stops the sequence on every channel at once, and the conversation passes to Daniel.' if outcome == 'Replies'
                else 'The booking stops the sequence on every channel at once; the meeting lifecycle takes over.')
    st.markdown(flow_html(p['steps'], active=active, states=states), unsafe_allow_html=True)
    phone = 'A phone number is bought, so text and voice can join the sequence.' if email == 'Yes' else \
        'No company email, so no phone number is bought (cost rule). The sequence runs on the channels it already has.'
    st.markdown(f'<div class="detail"><b>{esc(source)}</b> lands in the same pipeline as every other source. {esc(phone)} {esc(text)}</div>',
                unsafe_allow_html=True)


DANIEL_PATHS = {
    'Hi, I saw your ad. How does it work?': [
        ('agent', 'Happy to explain. Two quick questions so I point you to the right thing: what do you sell, and how do leads reach you today?'),
        ('lead', 'Real estate. Mostly Facebook leads, but we answer late.'),
        ('agent', 'That\'s exactly the gap we close. Want to see it on a 15-minute call? I have Tuesday 10:00 or Wednesday 14:00.'),
        ('lead', 'Wednesday works.'),
        ('agent', 'Booked for Wednesday 14:00. You\'ll get a confirmation now and a reminder a day before.'),
    ],
    'Can I talk to a person?': [
        ('agent', 'Of course. Connecting you with someone from the team now.'),
        ('person', 'Hi, I\'m here. How can I help?'),
    ],
}


def try_daniel():
    st.markdown('Pick how the lead opens. The messages are made up to show the two paths; on WhatsApp the real agent uses fixed wording.')
    opener = st.segmented_control('Lead writes', list(DANIEL_PATHS), default=list(DANIEL_PATHS)[0], key='dn_open')
    opener = opener or list(DANIEL_PATHS)[0]
    with st.container(border=True):
        st.markdown(f'<div class="who" style="text-align:right">Lead · WhatsApp</div><div class="bubble lead">{esc(opener)}</div>', unsafe_allow_html=True)
        for who, text in DANIEL_PATHS[opener]:
            name = {'agent': 'Daniel (agent)', 'person': 'Team member', 'lead': 'Lead'}[who]
            align = 'text-align:right' if who == 'lead' else ''
            st.markdown(f'<div class="who" style="{align}">{name}</div><div class="bubble {who}">{esc(text)}</div>', unsafe_allow_html=True)
    if opener == 'Can I talk to a person?':
        st.markdown('<div class="detail">A person takes over in the same conversation, and the agent goes quiet. The record is updated and the team is alerted.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="detail">Qualifying questions, then times, then a booking on the calendar. The record is updated and the meeting lifecycle starts.</div>', unsafe_allow_html=True)


def try_meeting():
    confirms = st.segmented_control('A day before the meeting, the lead…', ['confirms', 'doesn\'t confirm'], default='confirms', key='mt_conf')
    p = BY_ID['meeting']
    if confirms == 'doesn\'t confirm':
        st.markdown(flow_html(p['steps'], active=4, states={0: 'done', 1: 'done', 2: 'done', 3: 'done'}), unsafe_allow_html=True)
        st.markdown('<div class="detail">A person gets an alert and follows up. <b>The meeting is not cancelled automatically</b>, ever.</div>', unsafe_allow_html=True)
    else:
        st.markdown(flow_html(p['steps'], active=5, states={0: 'done', 1: 'done', 2: 'done', 3: 'done', 4: 'skip'}), unsafe_allow_html=True)
        st.markdown('<div class="detail">No alert needed. The status is updated to confirmed.</div>', unsafe_allow_html=True)


CRM_TEMPLATES = {'Webhook': 'Tested live.', 'HubSpot': 'Built; passed the readiness checks; not yet tested against a real account.',
                 'GoHighLevel': 'Built; passed the readiness checks; not yet tested against a real account.',
                 'Airtable': 'Built; passed the readiness checks; not yet tested against a real account.',
                 'Google Sheets': 'Built; passed the readiness checks; not yet tested against a real account.',
                 'CSV': 'Built; passed the readiness checks; not yet tested against a real account.'}


def try_crm():
    c1, c2, c3 = st.columns(3)
    dest = c1.selectbox('Client\'s CRM', list(CRM_TEMPLATES), key='crm_dest')
    ready = c2.segmented_control('Connection ready?', ['Yes', 'No'], default='Yes', key='crm_ready')
    exists = c3.segmented_control('Record already in the CRM?', ['No', 'Yes'], default='No', key='crm_dup')
    p = BY_ID['crm']
    if ready == 'No':
        st.markdown(flow_html(p['steps'], states={0: 'done', 1: 'stop', 2: 'skip', 3: 'skip', 4: 'skip', 5: 'skip'}), unsafe_allow_html=True)
        st.markdown('<div class="detail"><b>crm_hold</b> stops the sync. Nothing is sent half-ready, and the record waits until the connection is ready.</div>', unsafe_allow_html=True)
    else:
        st.markdown(flow_html(p['steps'], states={i: 'done' for i in range(6)}), unsafe_allow_html=True)
        action = 'the existing record is updated, not created twice' if exists == 'Yes' else 'a new record is created'
        st.markdown(f'<div class="detail">Fields are mapped with the <b>{esc(dest)}</b> template, {action}, and the sync is written to the log.</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="note">{esc(dest)} template status: {esc(CRM_TEMPLATES[dest])}</p>', unsafe_allow_html=True)


def try_proxy():
    st.markdown('Where each turn\'s fixed prompt (about 10,000 tokens) comes from, with and without the proxy.')
    on = st.toggle('Proxy on', value=True, key='px_on')
    rows = []
    for turn in range(1, 5):
        if not on:
            label, colour, width = 'whole prompt paid again', MUTED, 100
        elif turn == 1:
            label, colour, width = 'fixed part written to the cache', ACCENT, 100
        else:
            label, colour, width = 'fixed part read from the cache', OK, 18
        rows.append(f'<div style="display:flex;align-items:center;gap:10px;margin:6px 0"><span style="width:58px;font-size:14px">Turn {turn}</span>'
                    f'<span class="bar" style="width:{width * 0.55}%;background:{colour}"></span><span style="font-size:13.5px;color:{MUTED}">{label}</span></div>')
    st.markdown(''.join(rows), unsafe_allow_html=True)
    st.markdown('<p class="note">Bar lengths illustrate the idea, not exact prices. The measured result: about 5.2× lower cost on one sample 4-turn conversation.</p>', unsafe_allow_html=True)


JOB_GATES = ['Title rule', 'Excluded industry', 'Location rule', 'Seen before?', 'Two reviews', 'Verdict']
JOB_SAMPLES = [
    dict(name='Marketing Automation Manager · Tel Aviv', a=82, b=78,
         note='It passes every free rule.'),
    dict(name='Senior Backend Engineer · Tel Aviv', stop=0,
         note='Engineering titles are removed by a title rule, before any paid call.'),
    dict(name='Head of Product · Example Security Ltd', stop=1,
         note='The employer is in an excluded industry (a list I maintain), so it never reaches a review.'),
    dict(name='Product Manager · Barcelona, hybrid', stop=2,
         note='Outside Israel, a role is shown only if it is fully remote and written in English. This one is hybrid.'),
    dict(name='Marketing Automation Manager · Tel Aviv (posted again)', stop=3,
         note='Same company and title as a role I already applied to, so the re-posted ad does not come back.'),
    dict(name='AI Product Manager · Remote, Europe', a=66, b=52, third=58,
         note='"Remote, Europe" does not prove that someone based in Israel can be hired, so the two reviews read it differently.'),
    dict(name='Sales Development Rep · Haifa', a=33, b=29,
         note='It passes the free rules, but the match is low. A role under 40 is archived and never shown.'),
]
VERDICT_STYLE = {'Apply now': (OK_SOFT, OK), 'Apply': (ACCENT_SOFT, ACCENT), 'Maybe': (PART_SOFT, PART), 'Skip': (BAD_SOFT, BAD)}


def job_verdict(score, hard=False):
    if hard or score < 40:
        return 'Skip'
    return 'Apply now' if score >= 80 else 'Apply' if score >= 60 else 'Maybe'


def verdict_html(v):
    bg, fg = VERDICT_STYLE[v]
    return f'<span class="band" style="background:{bg};color:{fg};margin:0;vertical-align:baseline">{v}</span>'


def try_jobs():
    st.markdown('Pick a made-up role to see where the rules stop it, or what the reviews decide. These are illustrations, not real postings.')
    pick = st.selectbox('A role to follow', [s['name'] for s in JOB_SAMPLES], key='jb_pick')
    s = next(x for x in JOB_SAMPLES if x['name'] == pick)
    steps = [(g, '') for g in JOB_GATES]
    if 'stop' in s:
        k = s['stop']
        states = {i: 'done' for i in range(k)}
        states[k] = 'stop'
        states.update({i: 'skip' for i in range(k + 1, len(JOB_GATES))})
        calls = 0
        result = f'<b>Stopped at: {esc(JOB_GATES[k])}.</b> {esc(s["note"])}'
    else:
        gap = abs(s['a'] - s['b'])
        final = s['third'] if gap > 10 else round((s['a'] + s['b']) / 2)
        verdict = job_verdict(final)
        states = {i: 'done' for i in range(len(JOB_GATES))}
        if verdict == 'Skip':
            states[5] = 'stop'
        calls = 3 if gap > 10 else 2
        how = (f'Review A gave {s["a"]} and review B gave {s["b"]}. ' +
               (f'They differ by {gap} points, so a third review decides: {final}.' if gap > 10
                else f'They are within 10 points, so the match is their average: {final}.'))
        result = f'{esc(s["note"])}<br>{how} <b>Match {final}</b> {verdict_html(verdict)}'
    st.markdown(flow_html(steps, states=states), unsafe_allow_html=True)
    st.markdown(f'<div class="detail">{result}<div class="rule">Paid Claude calls for this role: <b>{calls}</b></div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="h3">Two reviews, one decision</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    a = c1.slider('Review A: match', 0, 100, 66, key='jb_a')
    b = c2.slider('Review B: match', 0, 100, 52, key='jb_b')
    gap = abs(a - b)
    if gap > 10:
        base = st.slider('Third review: it decides, no averaging', 0, 100, 58, key='jb_c')
        how = f'The reviews differ by {gap} points, more than 10, so a third review decides.'
    else:
        base = round((a + b) / 2)
        how = f'The reviews differ by {gap} points, 10 or less, so the match is their average.'
    hard = st.toggle('The post proves a hard eligibility conflict (for example, must live in the US)', key='jb_hard')
    final = min(base, 25) if hard else base
    verdict = job_verdict(final, hard)
    extra = (' A hard conflict caps the match at 25.' if hard else '') + (' A role under 40 is archived and never shown.' if final < 40 else '')
    st.markdown(f'<div class="detail">{esc(how)}{esc(extra)}<br><b>Match {final}</b> {verdict_html(verdict)}</div>', unsafe_allow_html=True)
    st.markdown('<p class="note">Apply now: 80 and up · Apply: 60 to 79 · Maybe: 40 to 59 · Skip: under 40, or a hard conflict.</p>', unsafe_allow_html=True)


TRY = {'icp': try_icp, 'scorers': try_scorers, 'cycle': try_cycle, 'daniel': try_daniel, 'meeting': try_meeting, 'crm': try_crm, 'proxy': try_proxy,
       'jobs': try_jobs}


# ---------- product page ----------

def product(pid):
    p = BY_ID[pid]
    i = [x['id'] for x in PRODUCTS].index(pid)
    nav = st.columns([1.4, 4, 1.2, 1.2], vertical_alignment='center')
    nav[0].button('← All products', on_click=go, args=('home',), key='back')
    nav[2].button('← Previous', on_click=go, args=(PRODUCTS[i - 1]['id'],), key='prev', disabled=i == 0, width='stretch')
    nav[3].button('Next →', on_click=go, args=(PRODUCTS[(i + 1) % len(PRODUCTS)]['id'],), key='next', disabled=i == len(PRODUCTS) - 1, width='stretch')

    rank = 'Bonus project' if p.get('bonus') else f'{i + 1} of {len(MAIN)}'
    st.markdown(f'<div class="rank">{rank}</div><h1 style="font-size:clamp(26px,4vw,38px);font-weight:800;margin:4px 0 6px">{esc(p["title"])}</h1>'
                f'<p class="lead">{esc(p["result"])}</p>{badge(p["status"])}', unsafe_allow_html=True)

    tab_how, tab_try, tab_why, tab_stack = st.tabs(['How it works', 'Try it', 'Problem & solution', 'Stack & proof'])

    with tab_how:
        st.caption('Tap a step to see what happens there.')
        labels = [f'{n + 1}' for n in range(len(p['steps']))]
        choice = st.segmented_control('Step', labels, default='1', key=f'step_{pid}', label_visibility='collapsed')
        n = int(choice or '1') - 1
        st.markdown(flow_html(p['steps'], active=n), unsafe_allow_html=True)
        label, detail = p['steps'][n]
        st.markdown(f'<div class="detail"><b>{n + 1:02d} · {esc(label)}</b><br>{esc(detail)}</div>', unsafe_allow_html=True)
        for name, text in p['rules']:
            st.markdown(f'<p class="rule"><b>{esc(name)}:</b> {esc(text)}</p>', unsafe_allow_html=True)

    with tab_try:
        TRY[pid]()

    with tab_why:
        c1, c2 = st.columns(2)
        c1.markdown(f'<div class="h3">The business problem</div><p>{esc(p["problem"])}</p>', unsafe_allow_html=True)
        c2.markdown(f'<div class="h3">The solution</div><p>{esc(p["solution"])}</p>', unsafe_allow_html=True)

    with tab_stack:
        st.markdown(''.join(f'<span class="chip">{esc(s)}</span>' for s in p['stack']) + '<br>' + badge(p['status']), unsafe_allow_html=True)
        if p['proof']:
            st.markdown(f'<p class="proof">{esc(p["proof"])}</p>', unsafe_allow_html=True)

    st.markdown('<div class="footer">Assaf Blitz · Tel Aviv · All products were designed and built with Claude Code.</div>', unsafe_allow_html=True)


if st.session_state.page in BY_ID:
    product(st.session_state.page)
else:
    home()
