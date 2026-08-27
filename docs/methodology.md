# Computational methodology

## Evidence classes

Every input and output is labelled as an `empirical_calibration`,
`empirical_nonestimate`, `illustrative_scenario`, or
`deterministic_test_vector`. Only Equations 11–13 reproduce a reported empirical
calibration. The other numeric examples exercise algebra or decision logic and
must not be interpreted as population estimates.

## Comparability gates

Equation 10 returns an RVR only when period, geography, asset perimeter, custody
perimeter, event definition, gross/net convention, valuation rule, exposure
concept, and reporting coverage match. The committed cash-versus-crypto row is
deliberately rejected. Equation 6 follows the same principle at the cohort level:
clearance, identification, arrest, prosecution, and conviction are not synonyms.

## Exposure and loss

Equation 8 evaluates the time integral by trapezoidal integration over strictly
ordered observations. Equation 9 reports value-weighted loss intensities, not the
probability that a particular currency unit is stolen. The 2019 cash denominator
is a transparent year-end-stock approximation, not average theft-exposed value.

## Cryptographic profiles

The XOR files are deterministic known-answer tests only. Production shares require
an independent CSPRNG, one-time use, authenticated envelopes, independent custody,
and a process that never logs the complete secret.

Shamir tests use the versioned `prime521-v1` profile over
$p=2^{521}-1$, so every 256-bit secret is a field element. Integers use big-endian
unsigned encoding; share indices are distinct non-zero field elements. This suite
does not claim a `GF(2^256)` profile. Adding one requires a vetted irreducible
degree-256 polynomial, an encoding specification, known-answer vectors, malformed
input tests, and independent review.

Secret sharing is not threshold signing and provides confidentiality, not share
authenticity. Supply-chain compromise, side channels, coercion, common-mode
failures, parser flaws, and recovery governance remain outside the algebraic
self-tests.

## Tail-risk calculation

Equation 21 uses the exact finite loss distribution: a common-mode event causes
total loss with probability $q$; otherwise the number of lost compartments is
binomial. Upper-tail CVaR includes fractional probability mass at the discrete
quantile boundary. The enumerated minimum is conditional on the committed scenario
parameters and feasible values of $N$.

