/*global fetch*/
import {
  GetSecretValueCommand,
  UpdateSecretCommand,
  SecretsManagerClient,
} from "@aws-sdk/client-secrets-manager";

export const handler = async (event, context, callback) => {
  // TODO implement
      let done = (err, res) => {
        if (err) {
            callback(null,
                {
                    statusCode: 400,
                    body: JSON.stringify({
                        type: "error",
                        err,
                    }),
                    headers: {
                        'Access-Control-Allow-Origin':'*' ,
                    "Access-Control-Allow-Headers":'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                    }

                });
        }
        else {
            callback(null,
                {
                    statusCode: 200,
                    body: JSON.stringify({
                        type: "success",
                        done: res
                    }),
                    headers: {
                    'Access-Control-Allow-Origin':'*' ,
                    "Access-Control-Allow-Headers":'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                    }
                });
        }
    };
        try {
            const client = new SecretsManagerClient({ region : "us-east-2"});
            const input = {
              SecretId: "dev/melomanie/spotify", // required
            };
            const command = new GetSecretValueCommand(input);
            const response = await client.send(command);
            let {client_id, client_secret, refresh_token, expires_at} = JSON.parse(response.SecretString);
            console.log(new Date(expires_at) < new Date(),new Date(expires_at),new Date() )
            if(new Date(expires_at) < new Date()){
                let url = 'https://accounts.spotify.com/api/token';
                let encoded = new Buffer.from(client_id + ':'+ client_secret).toString('base64');
                let params = {
                    grant_type: 'client_credentials'
                };
        
                const formParams = Object.keys(params).map((key) => {
                    return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
                }).join('&');
                
                const newTokenResult = await fetch(url, {
                    method: 'POST',
                    headers: {
                        "Authorization": 'Basic ' + encoded,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: formParams,
                })
                    .then((response) => {
                        console.log("we are here", response)
                        return response.json();
                    })
                    .catch((error) => {
                        done({
                            error: error
                        });
                    });
            // update the token in secret manager
            const expires_at = new Date(((new Date()).getTime()) + newTokenResult.expires_in * 1000)
            const updateInput = {client_id, client_secret, expires_at, refresh_token: newTokenResult.access_token}
            // console.log(expires_at)
            const updateCommand = new UpdateSecretCommand({
                "SecretId": input.SecretId,
                "SecretString": JSON.stringify(updateInput)
            });
            refresh_token = newTokenResult.access_token;
            await client.send(updateCommand);
            } 
            // now get recommendations
            const recommendParams = JSON.parse(event["body"])
            console.log(recommendParams);
            const formRecommendParams = Object.keys(recommendParams).map((key) => {
                    return encodeURIComponent(key) + '=' + encodeURIComponent(recommendParams[key]);
                }).join('&');
            const recommendationURL = `https://api.spotify.com/v1/recommendations?${formRecommendParams}`;
            const result = await fetch(recommendationURL, {
                    method: 'GET',
                    headers: {
                        "Authorization": 'Bearer ' + refresh_token,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                })
                    .then((response) => {
                        console.log("we are here --->", response)
                        return response.json();
                    })
                    .catch((error) => {
                        console.log(error);
                        done({
                            error: {
                                message: 'error while getting recommendation',
                                error: error,
                            }
                        });
                    });
                done(null,{result})
        }
            catch(error){
              console.log("error", error);
              return  done({
                            err: error?.error
                        });
            }
            
};
