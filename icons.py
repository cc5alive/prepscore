"""Line drawings for product cards. Our own artwork: shows the kind of item, not the exact product.

Each symbol is drawn on a 48x48 grid. Outlines use currentColor. Accent fills are inline styles
(var(--signal)), because page CSS can't reach inside a <use> copy.
"""

SYMBOLS = {
    "jug": '<rect style="fill:var(--signal);stroke:none" x="11" y="25" width="26" height="16" rx="2"/><rect x="10" y="14" width="28" height="28" rx="3"/><path d="M18 14V9h12v5M38 30h4v5h-4"/>',
    "barrel": '<rect style="fill:var(--signal);stroke:none" x="13" y="20" width="22" height="9"/><rect x="13" y="6" width="22" height="36" rx="4"/><path d="M13 16h22M13 32h22"/><circle cx="29" cy="11" r="1.5"/>',
    "filter": '<path style="fill:var(--signal)" d="M34 24s-6 7-6 11a6 6 0 0012 0c0-4-6-11-6-11z"/><rect x="10" y="10" width="11" height="26" rx="3"/><path d="M13 10V6h5v4M15.5 36v6M10 18h11M10 28h11"/>',
    "tablets": '<rect x="7" y="12" width="34" height="24" rx="3"/><circle style="fill:var(--signal)" cx="16" cy="20" r="3"/><circle style="fill:var(--signal)" cx="24" cy="20" r="3"/><circle style="fill:var(--signal)" cx="32" cy="20" r="3"/><circle style="fill:var(--signal)" cx="16" cy="28" r="3"/><circle style="fill:var(--signal)" cx="24" cy="28" r="3"/><circle cx="32" cy="28" r="3"/>',
    "powerstation": '<rect x="6" y="14" width="36" height="26" rx="3"/><path d="M16 14V9h16v5"/><rect x="11" y="21" width="7" height="9" rx="1"/><rect x="20" y="21" width="7" height="9" rx="1"/><rect style="fill:var(--signal)" x="30" y="21" width="7" height="6" rx="1"/><path d="M30 32h7"/>',
    "powerbank": '<rect x="14" y="6" width="20" height="36" rx="4"/><path style="fill:var(--signal)" d="M26 13l-7 12h5l-2 9 8-13h-5l2-8z"/>',
    "radio": '<rect x="6" y="16" width="36" height="24" rx="3"/><path d="M12 16L30 6M42 25h3v8h-3"/><circle cx="17" cy="28" r="6"/><rect style="fill:var(--signal)" x="27" y="21" width="10" height="5" rx="1"/><circle cx="29" cy="33" r="2"/><circle cx="35" cy="33" r="2"/>',
    "walkie": '<rect x="15" y="14" width="18" height="28" rx="3"/><path d="M19 14V4M20 31h8M20 35h8"/><rect style="fill:var(--signal)" x="19" y="18" width="10" height="8" rx="1"/>',
    "messenger": '<rect x="14" y="12" width="20" height="30" rx="5"/><path d="M28 12V6M37 9a6 6 0 013 5M40 5a11 11 0 015 9"/><rect style="fill:var(--signal)" x="18" y="17" width="12" height="9" rx="1"/><circle cx="24" cy="34" r="3"/>',
    "headlamp": '<path d="M8 28c0-9 7-15 16-15s16 6 16 15"/><rect style="fill:var(--signal)" x="17" y="20" width="14" height="11" rx="3"/><path d="M24 36v6M17 35l-3 5M31 35l3 5"/>',
    "lantern": '<path d="M18 10a6 6 0 0112 0M8 24h3M37 24h3"/><rect x="14" y="10" width="20" height="5" rx="2"/><rect style="fill:var(--signal)" x="16" y="15" width="16" height="18" rx="3"/><rect x="14" y="33" width="20" height="7" rx="2"/>',
    "firstaid": '<rect x="6" y="14" width="36" height="26" rx="3"/><path d="M18 14v-4h12v4"/><path style="fill:var(--signal)" d="M21 20h6v5h5v6h-5v5h-6v-5h-5v-6h5z"/>',
    "alarm": '<circle cx="24" cy="24" r="16"/><circle style="fill:var(--signal)" cx="24" cy="17" r="3"/><path d="M16 26h16M18 30h12M21 34h6"/>',
    "pouch": '<path d="M14 8h20l-2 6v26a2 2 0 01-2 2H18a2 2 0 01-2-2V14z"/><path d="M16 14h16"/><rect style="fill:var(--signal)" x="19" y="22" width="10" height="11" rx="1"/>',
    "foodbar": '<rect style="fill:var(--signal)" x="8" y="17" width="32" height="12" rx="2"/><rect x="10" y="29" width="28" height="10" rx="2"/><path d="M19 17v12M29 17v12"/>',
    "generator": '<path d="M8 36V14h32v22M5 36h38"/><rect style="fill:var(--signal)" x="12" y="19" width="14" height="13" rx="2"/><rect x="29" y="17" width="8" height="7" rx="2"/><circle cx="33" cy="30" r="2.5"/><circle cx="12" cy="40" r="3"/><circle cx="36" cy="40" r="3"/>',
    "solar": '<path style="fill:var(--signal);stroke:none" d="M10 10h28l4 22H6z"/><path d="M10 10h28l4 22H6zM8 21h32M19 10l-2 22M29 10l2 22M24 32v8M17 41h14"/>',
    "backpack": '<path d="M12 18a12 12 0 0124 0v20a3 3 0 01-3 3H15a3 3 0 01-3-3z"/><path d="M20 8a4 4 0 018 0"/><rect style="fill:var(--signal)" x="17" y="26" width="14" height="10" rx="2"/>',
    "multitool": '<path d="M30 25L42 14l2 2-10 10M15 25l-5-12 3-1 6 12"/><rect style="fill:var(--signal)" x="8" y="24" width="30" height="10" rx="5"/><circle cx="13" cy="29" r="1.5"/><circle cx="33" cy="29" r="1.5"/>',
    "book": '<path d="M8 10h12a4 4 0 014 4v26a3 3 0 00-3-3H8zM40 10H28a4 4 0 00-4 4v26a3 3 0 013-3h13z"/><path style="fill:var(--signal)" d="M31 10v11l3-2 3 2V10"/>',
    "blanket": '<rect x="8" y="13" width="32" height="8" rx="3"/><rect style="fill:var(--signal)" x="8" y="21" width="32" height="8" rx="3"/><rect x="8" y="29" width="32" height="8" rx="3"/>',
    "mylar": '<path style="fill:var(--signal)" d="M8 12l12-4 10 6 10-4v26l-10 4-10-6-12 4z"/><path d="M20 8v28M30 14v28"/>',
    "tourniquet": '<rect x="5" y="21" width="38" height="8" rx="4"/><rect style="fill:var(--signal)" x="21" y="8" width="6" height="34" rx="2"/><path d="M33 21v-6h5v6"/>',
    "carcharger": '<rect x="20" y="7" width="8" height="10" rx="1"/><path d="M18 17h12v21a3 3 0 01-3 3h-6a3 3 0 01-3-3z"/><rect style="fill:var(--signal)" x="21" y="23" width="6" height="3" rx="1"/><rect style="fill:var(--signal)" x="21" y="30" width="6" height="3" rx="1"/>',
    "canopener": '<path d="M15 42l8-17M23 42l5-17M36 16h7M39.5 12.5v7"/><circle cx="28" cy="16" r="8"/><circle style="fill:var(--signal)" cx="28" cy="16" r="3"/>',
    "stove": '<path style="fill:var(--signal)" d="M24 5c3 4 4 6 4 9a4 4 0 01-8 0c0-3 1-5 4-9z"/><path d="M12 28l4-8h16l4 8"/><rect x="8" y="28" width="32" height="10" rx="3"/><circle cx="15" cy="33" r="2"/>',
    "heater": '<rect x="8" y="9" width="32" height="30" rx="5"/><rect style="fill:var(--signal)" x="13" y="14" width="22" height="16" rx="2"/><path d="M13 19.5h22M13 24.5h22M12 39v3M36 39v3"/><circle cx="18" cy="34.5" r="1.5"/>',
    "sleepingbag": '<rect x="10" y="6" width="28" height="38" rx="9"/><ellipse style="fill:var(--signal)" cx="24" cy="15" rx="7" ry="5"/><path d="M31 23v16"/>',
    "gauze": '<path d="M20 36h18a4 4 0 004-4V22"/><circle cx="20" cy="24" r="12"/><circle style="fill:var(--signal)" cx="20" cy="24" r="4"/>',
    "mask": '<path style="fill:var(--signal)" d="M11 17c5-4 21-4 26 0l-2 13c-2 7-20 7-22 0z"/><path d="M11 19l-6-3M37 19l6-3M12 27l-6 4M36 27l6 4M24 14v24"/>',
    "docbag": '<path style="fill:var(--signal);stroke:none" d="M7 13l17 11 17-11z"/><rect x="6" y="12" width="36" height="26" rx="3"/><path d="M6 14l18 12 18-12"/>',
    "jumpstarter": '<rect x="8" y="14" width="22" height="28" rx="4"/><path style="fill:var(--signal)" d="M21 19l-6 10h4l-2 8 7-11h-4l2-7z"/><path d="M30 22h6l5-6M30 32h6l5 6"/>',
    "inflator": '<rect x="8" y="16" width="20" height="24" rx="4"/><circle style="fill:var(--signal)" cx="18" cy="26" r="5"/><path d="M28 22c9 0 12 4 12 10s-3 8-7 8M13 36h10"/>',
    "flare": '<path d="M10 30v-4c0-3 6-6 14-6s14 3 14 6v4"/><ellipse cx="24" cy="30" rx="14" ry="6"/><ellipse style="fill:var(--signal)" cx="24" cy="24" rx="8" ry="3"/><path d="M24 6v8M13 10l4 6M35 10l-4 6"/>',
    "toilet": '<path d="M12 21h24l-3 21H15z"/><ellipse style="fill:var(--signal)" cx="24" cy="18" rx="14" ry="4"/><path d="M18 30h12"/>',
    "bags": '<path style="fill:var(--signal);stroke:none" d="M14.5 30h19l.8 10H13.7z"/><path d="M14 14h20l2 28H12zM20 14l-2-6M28 14l2-6"/>',
    "petcarrier": '<rect x="6" y="14" width="36" height="26" rx="4"/><path d="M18 14V9h12v5"/><rect x="26" y="20" width="12" height="14" rx="1"/><path d="M30 20v14M34 20v14"/><circle style="fill:var(--signal)" cx="15" cy="28" r="4"/>',
}

# Black Friday products by ASIN.
BF_ICONS = {
    "B092FYPZ55": "jug", "B00B1OSU4W": "filter", "B0C5C89QKZ": "powerstation", "B0CXDXP8VR": "powerbank",
    "B015QIC1PW": "radio", "B09NQK87MN": "headlamp", "B0079ODGHO": "firstaid", "B004Y6V5CI": "alarm",
    "B084P7XXRJ": "pouch", "B0FM8653F1": "powerstation", "B0D6SQR1L1": "generator", "B0CNPHD4VY": "solar",
    "B09PSKG7C3": "messenger", "B0CZM49VLQ": "firstaid", "B08LP2CLJY": "backpack", "B079MJBP21": "multitool",
    "B0CVJ7R5BS": "filter", "0062378074": "book", "1496092589": "book", "B01IJWUYLK": "blanket",
    "B00176T9OY": "radio", "B01ITAKG6A": "tourniquet", "B0843SCLYH": "carcharger", "B00DZ1NFSK": "mylar",
    "B00004OCJW": "canopener", "B0D74164PZ": "jug", "B0CV9RPT8Y": "filter", "B09B2TVKGB": "tablets",
    "B06Y2H5GVX": "barrel", "B001CSAHW0": "foodbar", "B01HQRD8EO": "stove", "B07C23FB8S": "lantern",
    "B0GYT8HCT6": "heater", "B005EPRM4I": "sleepingbag", "B001WMFYH4": "walkie", "B07WW46HTF": "gauze",
    "B09FM2P1KF": "mask", "B08K34LMXP": "docbag", "B00475B96S": "backpack", "B015TKUPIC": "jumpstarter",
    "B07QR4Q42L": "inflator", "B07K3YFMVH": "flare", "B07Z2B1YYY": "toilet", "B07M863D89": "bags",
    "B00OP6SVJW": "petcarrier", "B07WRPCLYR": "firstaid", "0942364155": "book",
}


def sprite(keys):
    """Hidden inline SVG with one <symbol> per icon used on the page."""
    syms = "".join(f'<symbol id="i-{k}" viewBox="0 0 48 48">{SYMBOLS[k]}</symbol>' for k in sorted(set(keys)))
    return f'<svg class="icon-sprite" aria-hidden="true" focusable="false">{syms}</svg>'


def icon(key, cls="bf-ico"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{key}"/></svg>'
