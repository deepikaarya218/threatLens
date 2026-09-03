# from email import policy
# from email.parser import BytesParser
# from bs4 import BeautifulSoup
# import re
# import json
# import sys
# from pathlib import Path


# # =================================
# # HELPER: EXTRACT DOMAIN
# # =================================

# def extract_domain(value):
#     if not value:
#         return None

#     match = re.search(
#         r'@([A-Za-z0-9.-]+)',
#         str(value)
#     )

#     if match:
#         return match.group(1).lower()

#     return None


# # =================================
# # HEADER FORENSICS
# # =================================

# def analyze_header_forensics(msg):

#     # ---------------------------------
#     # IDENTITY
#     # ---------------------------------

#     from_header = msg.get("From")
#     reply_to_header = msg.get("Reply-To")
#     return_path_header = msg.get("Return-Path")

#     from_domain = extract_domain(from_header)
#     reply_to_domain = extract_domain(reply_to_header)
#     return_path_domain = extract_domain(return_path_header)

#     anomalies = []
#     is_spoofed = False

#     # From vs Reply-To mismatch
#     if (
#         from_domain
#         and reply_to_domain
#         and from_domain != reply_to_domain
#     ):
#         is_spoofed = True

#         anomalies.append({
#             "type": "Reply-To domain mismatch",
#             "severity": "High",
#             "details": (
#                 f"From domain is {from_domain}, "
#                 f"but Reply-To domain is {reply_to_domain}"
#             )
#         })

#     # From vs Return-Path mismatch
#     if (
#         from_domain
#         and return_path_domain
#         and from_domain != return_path_domain
#     ):
#         anomalies.append({
#             "type": "Return-Path domain mismatch",
#             "severity": "Medium",
#             "details": (
#                 f"From domain is {from_domain}, "
#                 f"but Return-Path domain is {return_path_domain}"
#             )
#         })

#     # ---------------------------------
#     # AUTHENTICATION RESULTS
#     # ---------------------------------

#     authentication_headers = msg.get_all(
#         "Authentication-Results",
#         []
#     )

#     raw_auth_header = "\n".join(
#         str(header)
#         for header in authentication_headers
#     )

#     auth_lower = raw_auth_header.lower()

#     spf = "unknown"
#     dkim = "unknown"
#     dmarc = "unknown"

#     # SPF
#     if "spf=pass" in auth_lower:
#         spf = "pass"
#     elif "spf=fail" in auth_lower:
#         spf = "fail"
#     elif "spf=softfail" in auth_lower:
#         spf = "softfail"
#     elif "spf=neutral" in auth_lower:
#         spf = "neutral"

#     # DKIM
#     if "dkim=pass" in auth_lower:
#         dkim = "pass"
#     elif "dkim=fail" in auth_lower:
#         dkim = "fail"
#     elif "dkim=neutral" in auth_lower:
#         dkim = "neutral"

#     # DMARC
#     if "dmarc=pass" in auth_lower:
#         dmarc = "pass"
#     elif "dmarc=fail" in auth_lower:
#         dmarc = "fail"
#     elif "dmarc=bestguesspass" in auth_lower:
#         dmarc = "bestguesspass"

#     # ---------------------------------
#     # NETWORK HOPS
#     # ---------------------------------

#     received_headers = msg.get_all(
#         "Received",
#         []
#     )

#     hop_chain = []
#     all_extracted_ips = []

#     for index, received in enumerate(
#         received_headers,
#         start=1
#     ):

#         received_string = str(received)

#         # Extract IPv4 addresses
#         ips = re.findall(
#             r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
#             received_string
#         )

#         # Add unique IPs
#         for ip in ips:
#             if ip not in all_extracted_ips:
#                 all_extracted_ips.append(ip)

#         hop_chain.append({
#             "hop_id": index,
#             "raw_received": received_string,
#             "extracted_public_ips": ips
#         })

#     # First extracted IP as origin candidate
#     origin_ip_candidate = (
#         all_extracted_ips[0]
#         if all_extracted_ips
#         else None
#     )

#     # ---------------------------------
#     # LIVE DNS VERIFICATION
#     # ---------------------------------
#     #
#     # Actual DNS lookup can be added later.
#     # For now we keep these as false defaults.
#     #

#     spf_record = False
#     dmarc_record = False

#     # ---------------------------------
#     # HEADER RISK SCORE
#     # ---------------------------------

#     header_risk_score = 0

#     if is_spoofed:
#         header_risk_score += 40

#     if spf == "fail":
#         header_risk_score += 20

#     if dkim == "fail":
#         header_risk_score += 20

#     if dmarc == "fail":
#         header_risk_score += 20

#     # Maximum score = 100
#     header_risk_score = min(
#         header_risk_score,
#         100
#     )

#     # ---------------------------------
#     # HEADER FINDINGS SUMMARY
#     # ---------------------------------

#     if anomalies:

#         header_findings_summary = (
#             f"{len(anomalies)} header anomaly(s) detected."
#         )

#     elif (
#         spf == "fail"
#         or dkim == "fail"
#         or dmarc == "fail"
#     ):

#         header_findings_summary = (
#             "Authentication failure detected in email headers."
#         )

#     else:

#         header_findings_summary = (
#             "No major header anomalies detected."
#         )

#     # ---------------------------------
#     # FINAL HEADER FORENSICS OBJECT
#     # ---------------------------------

#     header_forensics = {

#         "module": "B. HEADER FORENSICS",

#         "owner": "Akankcha",

#         "header_risk_score": header_risk_score,

#         "identity_analysis": {

#             "from_domain": from_domain,

#             "reply_to_domain": reply_to_domain,

#             "return_path_domain": return_path_domain,

#             "is_spoofed": is_spoofed,

#             "anomalies": anomalies
#         },

#         "authentication_matrix": {

#             "spf": spf,

#             "dkim": dkim,

#             "dmarc": dmarc,

#             "raw_auth_header": raw_auth_header
#         },

#         "live_dns_verification": {

#             "spf_record": spf_record,

#             "dmarc_record": dmarc_record
#         },

#         "network_hops": {

#             "total_hops": len(hop_chain),

#             "hop_chain": hop_chain,

#             "all_extracted_ips": all_extracted_ips,

#             "origin_ip_candidate": origin_ip_candidate
#         },

#         "header_findings_summary": header_findings_summary
#     }

#     return header_forensics


# # =================================
# # MAIN EMAIL PARSER
# # =================================

# def parse_email(file_path):

#     # ---------------------------------
#     # READ EML FILE
#     # ---------------------------------

#     with open(file_path, "rb") as f:

#         msg = BytesParser(
#             policy=policy.default
#         ).parse(f)

#     # ---------------------------------
#     # BASIC EMAIL HEADERS
#     # ---------------------------------

#     headers = {

#         "from": msg.get("From"),

#         "to": msg.get("To"),

#         "cc": msg.get("Cc"),

#         "bcc": msg.get("Bcc"),

#         "subject": msg.get("Subject"),

#         "date": msg.get("Date"),

#         "messageId": msg.get("Message-ID"),

#         "replyTo": msg.get("Reply-To"),

#         "returnPath": msg.get("Return-Path"),

#         "received": msg.get_all(
#             "Received",
#             []
#         )
#     }

#     # ---------------------------------
#     # EMAIL BODY
#     # ---------------------------------

#     plain_text = ""
#     html_text = ""

#     for part in msg.walk():

#         content_type = part.get_content_type()

#         if content_type == "text/plain":

#             try:

#                 plain_text += part.get_content()

#             except Exception:

#                 pass

#         elif content_type == "text/html":

#             try:

#                 html_text += part.get_content()

#             except Exception:

#                 pass

#     # ---------------------------------
#     # EXTRACT LINKS
#     # ---------------------------------

#     urls = set()

#     # URLs from plain text

#     plain_urls = re.findall(
#         r'https?://[^\s<>"\']+',
#         plain_text
#     )

#     for url in plain_urls:

#         urls.add(url)

#     # URLs from HTML

#     if html_text:

#         soup = BeautifulSoup(
#             html_text,
#             "html.parser"
#         )

#         for link in soup.find_all(
#             "a",
#             href=True
#         ):

#             href = link["href"]

#             if href.startswith(
#                 ("http://", "https://")
#             ):

#                 urls.add(href)

#     # Convert links to list

#     links = []

#     for url in sorted(urls):

#         # Extract domain
#         domain_match = re.search(
#             r'https?://([^/]+)',
#             url
#         )

#         domain = (
#             domain_match.group(1)
#             if domain_match
#             else None
#         )

#         links.append({

#             "url": url,

#             "domain": domain
#         })

#     # ---------------------------------
#     # EXTRACT ATTACHMENTS
#     # ---------------------------------

#     attachments = []

#     for part in msg.walk():

#         filename = part.get_filename()

#         if filename:

#             payload = part.get_payload(
#                 decode=True
#             )

#             attachment = {

#                 "filename": filename,

#                 "contentType": part.get_content_type(),

#                 "size": (
#                     len(payload)
#                     if payload
#                     else 0
#                 )
#             }

#             attachments.append(
#                 attachment
#             )

#     # ---------------------------------
#     # HEADER FORENSICS
#     # ---------------------------------

#     header_forensics = analyze_header_forensics(
#         msg
#     )

#     # ---------------------------------
#     # FINAL STRUCTURED EMAIL DATA
#     # ---------------------------------

#     result = {

#         "headers": headers,

#         "body": {

#             "plainText": plain_text,

#             "html": html_text
#         },

#         "links": links,

#         "attachments": attachments,

#         "headerForensics": header_forensics
#     }

#     return result


# # =================================
# # COMMAND LINE ENTRY POINT
# # =================================

# if __name__ == "__main__":

#     # ---------------------------------
#     # CHECK FILE ARGUMENT
#     # ---------------------------------

#     if len(sys.argv) < 2:

#         print(
#             json.dumps(
#                 {
#                     "error": "No .eml file provided"
#                 },
#                 indent=4
#             )
#         )

#         sys.exit(1)

#     # ---------------------------------
#     # GET FILE PATH
#     # ---------------------------------

#     file_path = Path(
#         sys.argv[1]
#     )

#     # ---------------------------------
#     # CHECK FILE EXISTS
#     # ---------------------------------

#     if not file_path.exists():

#         print(
#             json.dumps(
#                 {
#                     "error": (
#                         f"File not found: {file_path}"
#                     )
#                 },
#                 indent=4
#             )
#         )

#         sys.exit(1)

#     # ---------------------------------
#     # PARSE EMAIL
#     # ---------------------------------

#     try:

#         result = parse_email(
#             file_path
#         )

#         # ---------------------------------
#         # OUTPUT JSON
#         # ---------------------------------

#         formatted_json = json.dumps(

#             result,

#             ensure_ascii=False,

#             indent=4
#         )

#         sys.stdout.write(
#             formatted_json
#         )

#         sys.stdout.write("\n")

#     except Exception as e:

#         print(
#             json.dumps(
#                 {
#                     "error": str(e)
#                 },
#                 indent=4
#             )
#         )

#         sys.exit(1)


from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import re
import json
import sys
from pathlib import Path


# =================================
# HELPER: EXTRACT DOMAIN
# =================================

def extract_domain(value):

    if not value:
        return None

    match = re.search(
        r'@([A-Za-z0-9.-]+)',
        str(value)
    )

    if match:
        return match.group(1).lower()

    return None


# =================================
# HELPER: EXTRACT RECEIVED HEADERS
# =================================

def extract_received_headers(msg):

    received_headers = []

    # Robust case-insensitive extraction
    for key, value in msg.items():

        if key.lower() == "received":

            received_headers.append(
                str(value)
            )

    return received_headers


# =================================
# HELPER: EXTRACT PUBLIC IPs
# =================================

def extract_ipv4_addresses(text):

    if not text:
        return []

    ips = re.findall(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        text
    )

    valid_ips = []

    for ip in ips:

        parts = ip.split(".")

        if len(parts) != 4:
            continue

        try:

            if all(
                0 <= int(part) <= 255
                for part in parts
            ):
                if ip not in valid_ips:
                    valid_ips.append(ip)

        except ValueError:
            pass

    return valid_ips


# =================================
# HEADER FORENSICS
# =================================

def analyze_header_forensics(msg):

    # ---------------------------------
    # IDENTITY
    # ---------------------------------

    from_header = msg.get("From")
    reply_to_header = msg.get("Reply-To")
    return_path_header = msg.get("Return-Path")

    from_domain = extract_domain(
        from_header
    )

    reply_to_domain = extract_domain(
        reply_to_header
    )

    return_path_domain = extract_domain(
        return_path_header
    )

    anomalies = []

    is_spoofed = False

    # ---------------------------------
    # FROM vs REPLY-TO
    # ---------------------------------

    if (
        from_domain
        and reply_to_domain
        and from_domain != reply_to_domain
    ):

        is_spoofed = True

        anomalies.append({

            "type": "Reply-To domain mismatch",

            "severity": "High",

            "details": (
                f"From domain is {from_domain}, "
                f"but Reply-To domain is "
                f"{reply_to_domain}"
            )
        })

    # ---------------------------------
    # FROM vs RETURN-PATH
    # ---------------------------------

    if (
        from_domain
        and return_path_domain
        and from_domain != return_path_domain
    ):

        anomalies.append({

            "type": "Return-Path domain mismatch",

            "severity": "Medium",

            "details": (
                f"From domain is {from_domain}, "
                f"but Return-Path domain is "
                f"{return_path_domain}"
            )
        })

    # ---------------------------------
    # AUTHENTICATION RESULTS
    # ---------------------------------

    authentication_headers = msg.get_all(
        "Authentication-Results",
        []
    )

    raw_auth_header = "\n".join(
        str(header)
        for header in authentication_headers
    )

    auth_lower = raw_auth_header.lower()

    spf = "unknown"
    dkim = "unknown"
    dmarc = "unknown"

    # SPF
    if "spf=pass" in auth_lower:

        spf = "pass"

    elif "spf=fail" in auth_lower:

        spf = "fail"

    elif "spf=softfail" in auth_lower:

        spf = "softfail"

    elif "spf=neutral" in auth_lower:

        spf = "neutral"

    # DKIM
    if "dkim=pass" in auth_lower:

        dkim = "pass"

    elif "dkim=fail" in auth_lower:

        dkim = "fail"

    elif "dkim=neutral" in auth_lower:

        dkim = "neutral"

    # DMARC
    if "dmarc=pass" in auth_lower:

        dmarc = "pass"

    elif "dmarc=fail" in auth_lower:

        dmarc = "fail"

    elif "dmarc=bestguesspass" in auth_lower:

        dmarc = "bestguesspass"

    # ---------------------------------
    # RECEIVED HEADERS
    # ---------------------------------

    received_headers = extract_received_headers(
        msg
    )

    # ---------------------------------
    # NETWORK HOPS
    # ---------------------------------

    hop_chain = []

    all_extracted_ips = []

    for index, received in enumerate(
        received_headers,
        start=1
    ):

        received_string = str(
            received
        )

        ips = extract_ipv4_addresses(
            received_string
        )

        # Add unique IPs
        for ip in ips:

            if ip not in all_extracted_ips:

                all_extracted_ips.append(ip)

        hop_chain.append({

            "hop_id": index,

            "raw_received": received_string,

            "extracted_public_ips": ips
        })

    # ---------------------------------
    # ORIGIN IP CANDIDATE
    # ---------------------------------

    origin_ip_candidate = (

        all_extracted_ips[0]

        if all_extracted_ips

        else None
    )

    # ---------------------------------
    # LIVE DNS VERIFICATION
    # ---------------------------------
    #
    # Actual DNS lookup is not performed
    # in this parser yet.
    #

    spf_record = False

    dmarc_record = False

    # ---------------------------------
    # HEADER RISK SCORE
    # ---------------------------------

    header_risk_score = 0

    if is_spoofed:

        header_risk_score += 40

    if spf == "fail":

        header_risk_score += 20

    if dkim == "fail":

        header_risk_score += 20

    if dmarc == "fail":

        header_risk_score += 20

    header_risk_score = min(
        header_risk_score,
        100
    )

    # ---------------------------------
    # HEADER FINDINGS SUMMARY
    # ---------------------------------

    if anomalies:

        header_findings_summary = (

            f"{len(anomalies)} "
            "header anomaly(s) detected."
        )

    elif (
        spf == "fail"
        or dkim == "fail"
        or dmarc == "fail"
    ):

        header_findings_summary = (

            "Authentication failure detected "
            "in email headers."
        )

    elif received_headers:

        header_findings_summary = (

            f"{len(received_headers)} "
            "network hop(s) detected."
        )

    else:

        header_findings_summary = (

            "No major header anomalies detected."
        )

    # ---------------------------------
    # FINAL HEADER FORENSICS
    # ---------------------------------

    header_forensics = {

        "module": "B. HEADER FORENSICS",

        "owner": "Akankcha",

        "header_risk_score": header_risk_score,

        "identity_analysis": {

            "from_domain": from_domain,

            "reply_to_domain": reply_to_domain,

            "return_path_domain": return_path_domain,

            "is_spoofed": is_spoofed,

            "anomalies": anomalies
        },

        "authentication_matrix": {

            "spf": spf,

            "dkim": dkim,

            "dmarc": dmarc,

            "raw_auth_header": raw_auth_header
        },

        "live_dns_verification": {

            "spf_record": spf_record,

            "dmarc_record": dmarc_record
        },

        "network_hops": {

            "total_hops": len(hop_chain),

            "hop_chain": hop_chain,

            "all_extracted_ips": all_extracted_ips,

            "origin_ip_candidate": origin_ip_candidate
        },

        "header_findings_summary":
            header_findings_summary
    }

    return header_forensics


# =================================
# MAIN EMAIL PARSER
# =================================

def parse_email(file_path):

    # ---------------------------------
    # READ EML FILE
    # ---------------------------------

    with open(file_path, "rb") as f:

        msg = BytesParser(
            policy=policy.default
        ).parse(f)

    # ---------------------------------
    # RECEIVED HEADERS
    # ---------------------------------

    received_headers = extract_received_headers(
        msg
    )

    # ---------------------------------
    # BASIC EMAIL HEADERS
    # ---------------------------------

    headers = {

        "from": msg.get("From"),

        "to": msg.get("To"),

        "cc": msg.get("Cc"),

        "bcc": msg.get("Bcc"),

        "subject": msg.get("Subject"),

        "date": msg.get("Date"),

        "messageId": msg.get("Message-ID"),

        "replyTo": msg.get("Reply-To"),

        "returnPath": msg.get("Return-Path"),

        # IMPORTANT
        "received": received_headers
    }

    # ---------------------------------
    # EMAIL BODY
    # ---------------------------------

    plain_text = ""

    html_text = ""

    for part in msg.walk():

        content_type = (
            part.get_content_type()
        )

        if content_type == "text/plain":

            try:

                plain_text += (
                    part.get_content()
                )

            except Exception:

                pass

        elif content_type == "text/html":

            try:

                html_text += (
                    part.get_content()
                )

            except Exception:

                pass

    # ---------------------------------
    # EXTRACT LINKS
    # ---------------------------------

    urls = set()

    # Plain text URLs

    plain_urls = re.findall(

        r'https?://[^\s<>"\']+',

        plain_text
    )

    for url in plain_urls:

        urls.add(url)

    # HTML URLs

    if html_text:

        soup = BeautifulSoup(

            html_text,

            "html.parser"
        )

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link["href"]

            if href.startswith(
                ("http://", "https://")
            ):

                urls.add(href)

    # ---------------------------------
    # CONVERT LINKS TO LIST
    # ---------------------------------

    links = []

    for url in sorted(urls):

        domain_match = re.search(

            r'https?://([^/]+)',

            url
        )

        domain = (

            domain_match.group(1)

            if domain_match

            else None
        )

        links.append({

            "url": url,

            "domain": domain
        })

    # ---------------------------------
    # EXTRACT ATTACHMENTS
    # ---------------------------------

    attachments = []

    for part in msg.walk():

        filename = part.get_filename()

        if filename:

            payload = part.get_payload(
                decode=True
            )

            attachment = {

                "filename": filename,

                "contentType":
                    part.get_content_type(),

                "size": (
                    len(payload)
                    if payload
                    else 0
                )
            }

            attachments.append(
                attachment
            )

    # ---------------------------------
    # HEADER FORENSICS
    # ---------------------------------

    header_forensics = (
        analyze_header_forensics(msg)
    )

    # ---------------------------------
    # FINAL STRUCTURED DATA
    # ---------------------------------

    result = {

        "headers": headers,

        "body": {

            "plainText": plain_text,

            "html": html_text
        },

        "links": links,

        "attachments": attachments,

        "headerForensics":
            header_forensics
    }

    return result


# =================================
# COMMAND LINE ENTRY POINT
# =================================

if __name__ == "__main__":

    # ---------------------------------
    # CHECK FILE ARGUMENT
    # ---------------------------------

    if len(sys.argv) < 2:

        print(
            json.dumps(
                {
                    "error":
                        "No .eml file provided"
                },
                indent=4
            )
        )

        sys.exit(1)

    # ---------------------------------
    # FILE PATH
    # ---------------------------------

    file_path = Path(
        sys.argv[1]
    )

    # ---------------------------------
    # CHECK FILE EXISTS
    # ---------------------------------

    if not file_path.exists():

        print(
            json.dumps(
                {
                    "error": (
                        f"File not found: "
                        f"{file_path}"
                    )
                },
                indent=4
            )
        )

        sys.exit(1)

    # ---------------------------------
    # PARSE EMAIL
    # ---------------------------------

    try:

        result = parse_email(
            file_path
        )

        # ---------------------------------
        # OUTPUT JSON
        # ---------------------------------

        formatted_json = json.dumps(

            result,

            ensure_ascii=False,

            indent=4
        )

        sys.stdout.write(
            formatted_json
        )

        sys.stdout.write("\n")

    except Exception as e:

        print(
            json.dumps(
                {
                    "error": str(e)
                },
                indent=4
            )
        )

        sys.exit(1)