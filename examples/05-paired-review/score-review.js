// Outcome scorer shared by the no-skill and with-skill providers.
// A correct finding at the wrong file, or extra speculative findings, fails.
module.exports = (output, context) => {
  let review;
  try {
    review = typeof output === 'string' ? JSON.parse(output) : output;
  } catch (error) {
    return { pass: false, score: 0, reason: `Invalid JSON: ${error.message}` };
  }

  if (!review || !Array.isArray(review.issues)) {
    return { pass: false, score: 0, reason: 'Missing issues array' };
  }

  const actual = review.issues;
  const expectedKind = context.vars.expectedKind;
  const expectedFile = context.vars.expectedFile;
  if (expectedKind === 'none') {
    const pass = actual.length === 0;
    return {
      pass,
      score: pass ? 1 : 0,
      reason: pass ? 'Correctly reported a clean diff' : `False positives: ${actual.length}`,
    };
  }

  const matches = actual.filter(
    (issue) =>
      issue.kind === expectedKind &&
      issue.file === expectedFile &&
      Number.isInteger(issue.line) &&
      issue.line > 0 &&
      typeof issue.description === 'string' &&
      issue.description.trim().length >= 20 &&
      typeof issue.suggested_fix === 'string' &&
      issue.suggested_fix.trim().length >= 10,
  );
  const pass = matches.length === 1 && actual.length === 1;
  return {
    pass,
    score: pass ? 1 : 0,
    reason: pass
      ? `Found ${expectedKind} in ${expectedFile} without extra findings`
      : `Expected one ${expectedKind} in ${expectedFile}; got ${JSON.stringify(actual)}`,
  };
};
