# Hidayat Hadith Video Identity & Sequence Contract

## Locked generation rules
1. Every newly generated Hadith video receives the Hadith number as its primary sequence number.
2. Each Hadith book is a separate category/namespace.
3. The sequence is maintained independently inside each book.
4. The canonical identity is: <book>/<hadith-number>.
5. A video must not silently replace another Hadith number.
6. Recreate, duplicate, regenerate, or edit is ON DEMAND ONLY.
7. A new generation request must explicitly identify the target book and Hadith number.
8. If a canonical video already exists, the system must not generate a replacement automatically.
9. Edits create a revision of the same Hadith identity unless the user explicitly requests a new Hadith number.
10. Duplicate requests are treated as a deliberate user action, not an automatic retry.

## Example
- sahih-bukhari/2
- sahih-muslim/2
- sunan-abu-dawud/2

These are separate categories even though the Hadith number is the same.

## Review / publishing boundary
- Generated output goes to review.
- Human approval remains required.
- YouTube automatic publishing remains OFF.
- Failed jobs must not automatically recreate a video.
- Retries must not increment the Hadith number.

## Suggested metadata
{
  "book": "sahih-bukhari",
  "hadith_number": 2,
  "sequence_key": "sahih-bukhari/2",
  "revision": 1,
  "action": "generate",
  "recreate_on_demand": true,
  "auto_duplicate": false,
  "youtube_publish": false,
  "human_approval_required": true
}