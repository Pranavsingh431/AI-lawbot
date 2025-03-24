"""
Legal Glossary Component for the Legal Advisor AI.
"""

# Dictionary of legal terms and their definitions
LEGAL_GLOSSARY = {
    "Affidavit": "A written statement confirmed by oath or affirmation, for use as evidence in court.",
    
    "Arbitration": "A form of alternative dispute resolution where a dispute is submitted to one or more arbitrators who make a binding decision.",
    
    "Breach of Contract": "Violation of a contractual obligation, either by failing to perform one's promise or interfering with another party's performance.",
    
    "Case Law": "Law established by judicial decisions in cases, as distinct from laws created by legislatures.",
    
    "Damages": "Money claimed by, or ordered to be paid to, a person as compensation for loss or injury.",
    
    "Due Process": "The legal requirement that the state must respect all legal rights owed to a person, including the right to fair treatment through the normal judicial system.",
    
    "Force Majeure": "Unforeseeable circumstances that prevent someone from fulfilling a contract, often used as a clause in contracts to remove liability for natural and unavoidable catastrophes.",
    
    "Habeas Corpus": "A writ requiring a person under arrest to be brought before a judge or into court to secure the person's release unless lawful grounds are shown for detention.",
    
    "Indemnity": "Security or protection against a loss or other financial burden; a legal exemption from liability for damages.",
    
    "Jurisdiction": "The official power to make legal decisions and judgments; the territory or subject matter over which legal authority extends.",
    
    "Liability": "The state of being legally responsible for something, such as a debt, obligation, or responsibility.",
    
    "Negligence": "Failure to take proper care in doing something, resulting in damage or injury to another.",
    
    "Plaintiff": "A person who brings a case against another in a court of law.",
    
    "Precedent": "A decided case that furnishes a basis for determining later cases involving similar facts or issues.",
    
    "Tort": "A civil wrong that causes someone else to suffer loss or harm, resulting in legal liability for the person who commits the act.",
}

def get_legal_glossary_html():
    """
    Generate HTML for the legal glossary.
    
    Returns:
        str: HTML representation of the legal glossary
    """
    html = """
    <div class="legal-glossary">
        <ul style="list-style-type: none; padding-left: 0;">
    """
    
    # Add each term and definition
    for term, definition in sorted(LEGAL_GLOSSARY.items()):
        html += f"""
        <li style="margin-bottom: 12px;">
            <span style="font-weight: 600; color: var(--legal-term-color);">{term}</span>: 
            <span style="color: #333; font-size: 0.95em;">{definition}</span>
        </li>
        """
    
    html += """
        </ul>
    </div>
    """
    
    return html


def get_random_legal_term():
    """
    Get a random legal term and its definition.
    
    Returns:
        tuple: (term, definition)
    """
    import random
    terms = list(LEGAL_GLOSSARY.items())
    return random.choice(terms) 