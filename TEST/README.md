# Test Module

## Scenarios

- found
  - prepare `db` containing only the n-th article
    - replace existing `db`
  - query n-th article and commit it
- !found
  - prepare `db` with no article
    - replace existing `db`
  - query max no. of articles and commit

### CHECKS

> queried article objects in chronological order
> committed articles in chronological order

# Extras

- raw datetime is not ordered (AM/PM < 24hr)
