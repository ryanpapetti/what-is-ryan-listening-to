# install dependencies

pip install requests --target .

# zip the code
zip -rq function.zip *

# create the function
# aws lambda create-function \
# --function-name $(basename $(pwd)) \
# --zip-file fileb://function.zip \
# --profile ryanprofessional \
# --region us-west-2 \
# --runtime python3.9 \
# --role arn:aws:iam::375398450526:role/lambda-admin-role \
# --handler lambda_function.lambda_handler

# update the function
aws lambda update-function-code \
--function-name $(basename $(pwd)) \
--zip-file fileb://function.zip \
--profile ryanprofessional \
--region us-west-2

rm -rf !("deploy_function.sh"|"lambda_function.py")
