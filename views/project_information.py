"""
PAGE 7: PROJECT INFORMATION
Redesigned to match the enterprise SaaS design system (Image 2).
Academic project specification, architecture pipeline, mathematical foundations,
and comparative advantages.
"""

import streamlit as st


def render_project_information():
    """Render Page 7: Project Information & Academic Documentation."""
    st.markdown("""
        <div class="welcome-section">
            <div>
                <div class="welcome-title">Project Documentation & <span class="welcome-gradient-text">Architecture</span> ⓘ</div>
                <div class="welcome-subtitle">Academic project specification, theoretical foundations, mathematical formulation, and system design</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section 1: Executive Overview & Problem Statement
    st.markdown("""
        <div class="saas-card">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="color: #A78BFA; font-size: 1.1rem;">📌</span>
                    <span class="saas-card-title">1. Project Introduction & Problem Definition</span>
                </div>
            </div>
            <p style="color: #E2E8F0; line-height: 1.7; font-size: 0.92rem; margin-bottom: 0.75rem;">
                The explosive expansion of electronic messaging via Short Message Service (SMS) and Email 
                has catalyzed an unprecedented surge in malicious cyber activity. Unsolicited commercial advertising, 
                advance-fee fraud, banking phishing scams, lottery deceptions, and credential-harvesting lures inflict 
                billions of dollars in damages worldwide annually.
            </p>
            <p style="color: #A1A1AA; line-height: 1.7; font-size: 0.88rem;">
                <b>The Core Challenge:</b> Manual inspection is infeasible given communication velocity. Static keyword filters 
                are trivially evaded using homoglyphs, deliberate misspellings (<code>c@sh</code>, <code>fr33</code>), 
                or casual conversational syntax, while legitimate transactional emails (invoices, receipts) are frequently misflagged. 
                A resilient statistical machine learning approach is required to evaluate contextual word co-occurrences.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Section 2: Objectives & Existing vs Proposed System
    col_obj1, col_obj2 = st.columns(2)

    with col_obj1:
        st.markdown("""
            <div class="saas-card" style="height: 100%;">
                <div class="saas-card-header">
                    <div class="saas-card-title-group">
                        <span style="color: #F05268;">⚠️</span>
                        <span class="saas-card-title">Limitations of Conventional Systems</span>
                    </div>
                </div>
                <ul style="color: #E2E8F0; font-size: 0.86rem; line-height: 1.7; padding-left: 1.2rem;">
                    <li><b>Rigid Keyword Blacklists:</b> Severe false positive rate on legitimate corporate correspondence.</li>
                    <li><b>Zero Probabilistic Modeling:</b> Incapable of expressing statistical uncertainty or confidence.</li>
                    <li><b>No N-gram Awareness:</b> Fails to capture multi-word correlations ("verify" + "account" + "login").</li>
                    <li><b>High Maintenance Overhead:</b> Constant manual rule patching required.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col_obj2:
        st.markdown("""
            <div class="saas-card" style="height: 100%;">
                <div class="saas-card-header">
                    <div class="saas-card-title-group">
                        <span style="color: #22C55E;">✓</span>
                        <span class="saas-card-title">Proposed Intelligent Solution</span>
                    </div>
                </div>
                <ul style="color: #E2E8F0; font-size: 0.86rem; line-height: 1.7; padding-left: 1.2rem;">
                    <li><b>Multinomial Naive Bayes Engine:</b> Empirical class likelihood distributions calculated across 5,000 features.</li>
                    <li><b>Sublinear TF-IDF with Bigrams:</b> Penalizes ubiquitous stopwords while magnifying discriminating scam terms.</li>
                    <li><b>Transparent Threat Heuristics:</b> Distinguishes ML confidence from rule-based urgency cues.</li>
                    <li><b>Privacy by Architecture:</b> Zero plaintext caching mode ensures sensitive communication privacy.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Section 3: Architecture Diagram Card
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="saas-card">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="color: #8B5CF6;">⚙️</span>
                    <span class="saas-card-title">2. System Architecture & Information Pipeline</span>
                </div>
            </div>
            <div style="background-color: #211E29; border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.2rem; font-family: var(--font-family-mono); font-size: 0.82rem; color: #C4B5FD; line-height: 1.8;">
                [Incoming SMS / Email Payload] ──► [Unicode & Regex Token Normalization]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br>
                [Inference Prediction] ◄── [Multinomial Naive Bayes] ◄── [TF-IDF / N-gram Vectorizer]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► [Posterior Class Probabilities (Spam vs Ham)]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► [Heuristic Rule-Based Phishing & Urgency Evaluator]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► [SQLite Telemetry & Persistent Classification Audit Trail]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──► [Streamlit SaaS UI (Live Gauges, Plotly Charts & Activity Feed)]
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section 4: Mathematical Methodology
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="saas-card">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="color: #38BDF8;">📐</span>
                    <span class="saas-card-title">3. Mathematical Foundations</span>
                </div>
            </div>
            
            <h4 style="color: #F8FAFC; margin-bottom: 0.3rem; font-size: 0.95rem;">A. Bayes' Theorem for Document Classification</h4>
            <p style="color: #A1A1AA; font-size: 0.86rem;">
                Given a message represented as a feature vector <b>x</b> = (x₁, x₂, ..., xₙ), 
                the posterior probability of class <i>y</i> (where <i>y</i> ∈ {SPAM, HAM}) is:
            </p>
            <div style="background-color: #211E29; padding: 0.65rem 1rem; border-radius: 8px; border-left: 3px solid #8B5CF6; font-family: monospace; font-size: 0.9rem; margin-bottom: 1rem;">
                P(y | x) = [ P(y) × P(x | y) ] / P(x)
            </div>

            <h4 style="color: #F8FAFC; margin-bottom: 0.3rem; font-size: 0.95rem;">B. Multinomial Naive Bayes Conditional Independence</h4>
            <p style="color: #A1A1AA; font-size: 0.86rem;">
                Assuming conditional feature independence given class <i>y</i>:
            </p>
            <div style="background-color: #211E29; padding: 0.65rem 1rem; border-radius: 8px; border-left: 3px solid #A78BFA; font-family: monospace; font-size: 0.9rem; margin-bottom: 1rem;">
                P(x | y) = ∏ P(xᵢ | y)
            </div>

            <h4 style="color: #F8FAFC; margin-bottom: 0.3rem; font-size: 0.95rem;">C. Laplace (Lidstone) Smoothing</h4>
            <p style="color: #A1A1AA; font-size: 0.86rem;">
                To eliminate zero-frequency probabilities for unseen words during inference, Laplace smoothing with α = 0.1 is applied:
            </p>
            <div style="background-color: #211E29; padding: 0.65rem 1rem; border-radius: 8px; border-left: 3px solid #22C55E; font-family: monospace; font-size: 0.9rem;">
                θ_yi = ( N_yi + α ) / ( N_y + α × |V| )
            </div>
        </div>
    """, unsafe_allow_html=True)
