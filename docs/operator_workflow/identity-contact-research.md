# Prospect Identity and Contact Research

This procedure covers three related operator workflows:

1. Identity Research establishes enough company context to understand the prospect.
2. Primary-contact Selection determines which roles are the best outreach targets for that specific prospect.
3. Contact Research identifies real people and reliable contact channels for those selected roles.

Keep these decisions separate. Choosing a role does not identify a person. Identifying a person does not prove that person is relevant to the prospect's signal. Finding a company email does not prove the email belongs to a particular person.

## A. Identity Research

### Purpose

Identity Research establishes a reliable company profile before contact-targeting decisions are made. The research should provide enough organizational context to understand what kind of prospect this is, how large and structured the organization is, and which public identities may be useful during later contact research.

Complete Identity Research before Primary-contact Selection whenever possible because company size and structure materially affect which contact roles are appropriate.

### 1. Use the organization's canonical name

`prospect_name` must be the canonical public name of the organization or entity represented by the Prospect record. A Prospect represents the organization, not the product, platform, system, migration, initiative, signal, location, or research path that caused it to be discovered.

Do not append qualifiers such as product names, business units, launches, migrations, or parenthetical research labels to `prospect_name`. For example:

- use `Microsoft`, not `Microsoft Foundry`;
- use `SAP`, not `SAP SuccessFactors - Latest People Profile`;
- use `National University`, not `National University - Student Information System`.

Store product and initiative names in Signals, prospect metadata, source notes, positioning fields, or other appropriate context fields. Use the organization's official website and organization-level normalized domain when available.

Before creating a Prospect, search for an existing organization-level record by normalized domain, website, and canonical name. Do not create separate Prospects for different products or initiatives owned by the same organization unless they are genuinely separate legal or operating entities that should be contacted and tracked independently.

### 2. Flesh out the Identity section

Research and populate the available first-class identity fields wherever reliable information can be found.

At minimum, research:

- official website
- prospect type
- official LinkedIn company profile
- official X/Twitter account
- employee count or useful company-size estimate

Also capture other stable identity information when it improves identification or later targeting.

#### Website

Identify the company's actual official website. Prefer the company's own site or a domain linked from another verified company-controlled profile. Do not substitute a job-board page, directory profile, or social profile when an official domain can be established.

#### Prospect type

Classify the organization according to what it actually is, not according to where it was discovered. Consider what the company sells, who it serves, its size, and whether it is a startup, SMB, enterprise, agency, ecosystem partner, or another managed prospect type.

#### LinkedIn

Record the official company LinkedIn page. Verify that it represents the same organization by corroborating the website, branding, description, location, or other identifying details. Do not substitute an employee profile or job posting.

#### X / Twitter

Record the official company account when one can be established from first-party links or clear company-controlled branding. Leave the value absent rather than guessing from a plausible username.

#### Employee count

Record a defensible current size or range from sources such as LinkedIn, official company material, or other reliable recent sources. Avoid false precision. Company size is especially important because it informs Primary-contact Selection.

#### Other useful identity facts

Capture other stable facts when they improve prospect identification or contact targeting, for example headquarters, founding year, industry, funding stage, parent company, relevant product names, or alternate company names.

Do not turn identity metadata into a general research dump. Signal evidence, contact-research reasoning, and speculative notes belong elsewhere.

### 3. Put non-schema identity facts into prospect metadata

When useful identity information has no appropriate first-class `SEI Prospect` field, store it in the prospect metadata table.

Use consistent, reusable metadata names and concise values. Examples:

```text
LinkedIn -> https://www.linkedin.com/company/example
X -> https://x.com/example
Employee Count -> 51-200
Headquarters -> New York, NY
Founded -> 2021
```

Do not store speculation, unverified guesses, signal evidence, or long-form research notes as identity metadata.

### Completion standard

Identity Research is complete when the company has been reliably identified, the required identity fields have been researched, useful additional facts have been preserved as metadata where appropriate, and unsupported values have been left blank rather than guessed.

## B. Primary-contact Selection

### Purpose

Primary-contact Selection determines which roles Cartertek should actively try to reach at a particular prospect.

The playbook defines the available contact-role universe. Primary-contact Selection narrows that universe for the individual prospect by asking:

> Given this prospect's signal, company size, and organizational structure, which roles are close enough to the problem and senior enough to act on it?

This is a role-selection process, not a person-search process.

### 1. Select primary roles separately for each prospect

Do not automatically mark every playbook role primary, and do not reuse the same primary-role combination merely because multiple prospects share a playbook.

Review each prospect individually using:

- identity and employee count
- organizational structure
- prospect type
- observed signal
- likely affected team or function
- the playbook's available contact roles

Select only the subset of roles that make sense as actual outreach targets for that prospect.

A role can remain a valid playbook role without being a primary role for every prospect using that playbook.

### 2. Select for organizational proximity, not maximum seniority

The best contact is not necessarily the most senior person. Prefer roles that are both close enough to understand or experience the problem and senior enough to influence a response.

For a small founder-led company, Founder or CTO may directly own the technical work and be an appropriate primary target.

For a mid-sized company, VP Engineering, Engineering Manager, Product Lead, Technical Lead, or CTO may be better depending on the signal and affected area.

For a large organization, avoid defaulting to the founder, CEO, or top executive simply because they have authority. The better target may be the product leader, hiring manager, engineering leader, or technical owner closest to the affected initiative.

Use the signal to choose the relevant organizational layer, but do not infer that any particular person is signal-relevant during this process. Person-level relevance is established during Contact Research.

### 3. Primary status represents selected roles, not just known people

A primary-role decision must survive independently of whether a specific person has already been identified.

When a selected role already has a suitable contact row, mark that contact primary.

When no person has yet been identified, preserve the role-selection decision as an unresolved primary contact target rather than inventing a person. In the current Address Book model, a role-only row must include a meaningful note so it is treated as a real research target rather than an empty placeholder. For example:

```text
Primary contact role selected for this prospect; specific person and contact details still need to be identified.
```

Do not put an invented name, guessed email, or person-specific `signal_relevance` on an unresolved role target.

### 4. At completion, only selected roles may remain primary

Normalize the Address Book after making the role-selection decision.

- Contacts whose roles are selected primary targets may be marked primary.
- Contacts whose roles are not selected primary targets must not remain primary merely because they were previously researched, have an email, or are senior.
- Multiple roles may be primary when the prospect warrants multiple outreach paths.

The final primary flags should exactly represent the role-selection decision for that prospect.

### Completion standard

Primary-contact Selection is complete when the prospect has been evaluated individually, company size and organizational proximity were considered, primary roles are drawn from the prospect's playbook, and the Address Book's primary state represents only those selected targets.

## C. Contact Research

### Purpose

Contact Research turns selected contact roles into actual outreach paths.

A useful contact record must accurately represent:

1. a real person or legitimate company-level contact route;
2. the person's actual role;
3. when the playbook role requires it, that person's connection to the prospect's signal; and
4. contact information genuinely attributable to that person or company route.

Research quality takes precedence over filling every field.

### Research rules

#### Use the playbook to constrain acceptable roles

Research contacts within the roles defined by the prospect's playbook. Do not add arbitrary executives or employees merely because their contact information is easy to find.

A person's exact job title does not need to equal the managed SEI role name, but the mapping must be substantively valid. For example, `Head of Product` may reasonably map to `Product Lead`; an unrelated manager should not be stretched into a technical role simply to make the candidate fit.

#### Verify the person actually occupies the claimed role

Before saving a named contact, establish that the person currently occupies, or is a clear equivalent of, the assigned SEI role.

Prefer current, attributable evidence such as:

- official company leadership or team pages
- company announcements
- the person's public professional profile
- founder or team biographies
- other reliable first-party or strongly attributable sources

Watch for stale sources. Do not represent a former employee, advisor, investor, or unrelated manager as a current role-holder because an old search result exists.

#### Never attach a generic company email to a named person

An email belongs in a named person's `emails` field only when there is evidence that the address belongs to that person.

Addresses such as `hello@`, `info@`, `contact@`, `support@`, `press@`, `sales@`, `recruiting@`, `careers@`, or `legal@` are normally company-level routes. Do not attach them to a founder, CTO, or other named person merely because that person works at the company.

#### Preserve useful generic emails as separate company contacts

Generic company routes are still useful. Store them separately from named people, using an appropriate company/general contact row and notes that describe the route.

For example:

```text
Role: Primary Contact
Name:
Email: hello@example.com
Notes: General company inbox published on the official website.
```

A prospect may therefore have both a named founder and a separate company-level contact route without falsely claiming that the company inbox belongs to the founder.

#### Do not guess personal email addresses

Never construct an email from a company pattern, another employee's address, a masked address, a partially displayed result, or an email-finder prediction.

For example, `j***n@example.com` does not justify saving `john@example.com`.

It is better to leave the email blank than to populate a plausible but unsupported address.

#### Prefer directly verifiable, publicly attributable emails

Prefer sources that expose the full email and tie it to the person, such as an official company profile, personal website, public resume or CV, founder-authored page, conference biography, public developer listing, public technical/community profile, or similar attributable source.

A publicly posted personal address may be retained when useful, but describe it honestly in the notes rather than presenting it as an official company-domain business address.

Retain enough source context in notes that important claims can be audited later.

### Process

#### 1. Prioritize research on primary contacts

Begin with the roles selected during Primary-contact Selection.

For each primary target:

1. find a current person occupying that role or a defensible equivalent;
2. verify the person's position;
3. populate the selected primary contact target with the verified person;
4. research person-specific contact channels; and
5. preserve the primary-role target for future research when no suitable person can yet be established.

Do not replace a strategically better primary role with an easier-to-find non-primary executive merely because the executive has a visible email.

Once a strong named primary contact is identified, prefer enriching that contact rather than repeatedly substituting weaker candidates whose emails are easier to find.

#### 2. Distinguish broad roles from signal-specific roles

Not every role requires the same person-level relevance test.

Broad roles can be inherently relevant because their remit covers the affected organization. Examples may include a CTO or a founder at a small company.

Signal-specific roles only become useful when the particular person is connected to the area represented by the prospect signal. These can include roles such as VP Engineering, Engineering Manager, Product Lead, or Technical Lead depending on the playbook's managed role definition.

The managed playbook contact-role configuration is authoritative for whether a role requires signal-specific relevance.

#### 3. Use `signal_relevance` to explain why this person is relevant

The playbook already establishes why the role is relevant. `signal_relevance` must establish why the specific named person is relevant to the specific prospect signal.

Do not write generic role commentary such as:

```text
Engineering Managers are relevant because they own engineering delivery.
```

Instead record the evidence-backed relationship, for example:

```text
Leads the engineering team currently hiring the role identified in the prospect's failed-recruitment signal.
```

Useful person-to-signal connections include evidence that the person:

- leads the team hiring the relevant role;
- owns the product or system implicated by the signal;
- publicly describes responsibility for the affected workflow;
- is personally recruiting for the relevant position; or
- leads the engineering function experiencing the observed bottleneck.

#### 4. Never create a person-level relevance claim for an unidentified contact

`signal_relevance` is person-level information. An unresolved primary role target may exist, but an unidentified person cannot have person-level relevance.

Do not write hypothetical statements such as:

```text
A Product Lead would likely own this workflow.
```

That only restates why the role exists in the playbook. Leave `signal_relevance` blank until an actual person is identified and their relationship to the signal is established.

#### 5. `signal_relevance` must affirmatively establish relevance

Do not use `signal_relevance` for uncertainty such as `may oversee`, `possibly relevant`, `could own`, `likely involved`, or `relevance needs verification`.

For a named contact occupying a signal-specific role, there are two acceptable outcomes:

- **Relevance established:** keep the person and record the specific evidence-backed relationship in `signal_relevance`.
- **Relevance not established:** do not treat that person as the validated contact for the primary role. Remove the unsupported person-level claim while preserving the underlying primary-role target for continued research.

The operator should treat these as separate evidence steps:

```text
Primary role selected
-> person identified for role
-> person-to-signal relevance established when required
-> contact channel verified
```

Success at one step does not prove the next.

### Completion standard

Contact Research is in a strong state when:

- research focused first on selected primary roles;
- named contacts actually occupy their assigned roles;
- signal-specific contacts have affirmative person-level `signal_relevance` when required;
- unresolved role targets contain no invented person-level relevance;
- direct emails are attributable to the named person;
- generic company emails are stored separately;
- no email was inferred from a pattern or masked result; and
- source context is preserved well enough to audit important contact claims.
