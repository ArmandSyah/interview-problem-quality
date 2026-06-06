# Test design rules

Tests should reveal pattern understanding, not just happy-path correctness.

Include cases for:

- Empty or minimal input if allowed.
- Single-element input when relevant.
- Duplicates.
- Negative values when allowed.
- Sorted and reverse-sorted inputs when relevant.
- Repeated collisions for hash map or sliding window problems.
- Boundary cases.
- Cases that break common incorrect approaches.

Accepted problems should generally have 6-10 Python tests. Drafts can temporarily have 3-5 tests,
but cannot be accepted until the accepted-stage threshold is met.

Reject or park problems when:

- Multiple outputs are valid but no custom checker exists.
- Expected outputs depend on randomness, timing, external state, or unspecified tie-breaking.
- Tests can be passed by a trivial hard-coded or shallow strategy.
- The problem needs floating-point tolerance before the runtime supports it.
