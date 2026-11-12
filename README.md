# What is Ryan listening to?

The public `/current-listen` endpoint invokes the `RyanCurrentListen` Express
state machine through API Gateway. The workflow obtains Spotify authorization
headers, then invokes this Lambda to fetch the currently playing track. API
Gateway extracts the final response body and sets the HTTP response headers.

## Logging

The workflow passes a Spotify access token between tasks. Keep Step Functions
execution-data logging disabled (`includeExecutionData: false`) so input and
output payloads are not included in new execution logs. The live workflow keeps
its `ALL` event level and existing CloudWatch Logs destination for operational
visibility. Its AWS configuration is managed outside this repository.

This setting does not remove logs created before it was disabled. Treat existing
execution logs as potentially sensitive and avoid logging tokens or headers in
Lambda code.

## Tests

Run `python3 -m unittest -v`.

## Deployment

GitHub Actions tests and builds the Lambda package on pull requests. A push to
`main` also deploys the package to `what-is-ryan-listening-to` in `us-west-2`.
The deploy job uses a GitHub OIDC role scoped to this repository's main branch
and this Lambda; it does not use long-lived AWS credentials. Revert a change on
`main` to deploy the reverted code.
