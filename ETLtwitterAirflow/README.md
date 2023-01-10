
### This is a basic ETL example using Twitter's Api and an AWS apache-airflow integration. 

There are some *enviroment* values that you have to get and appropiately fill the values. These are:
> - *owner* in the dag file <br>
> - *user* in the etl file <br>

Also you want to go to [https://developer.twitter.com/en/docs/twitter-api](https://) and get the correspondant keys. These are:
> - *acces_key* <br>
> - *access_secret* <br>
> - *consumer_key* <br>
> - *consumer-secret* <br>

Use the tweepy functions *OAuthHandler* and *set_access_token* to create the connection (*tweepy.API(auth)*). After that it is only about creating the api object that we will sneak (I will use the *api.user_timeline* function for this example, you could also check for other objects that you can use).

After that it is only about appending the elements in the list with the given attributes in our scope and saving the *db* in the csv file *refined_tweets.csv*.

Then one would have to go to *ec2* in **AWS** and launch an instance (Linux would be OK and free tier is OK as well also create the pertinent Key pair and allow the *HTTP*, and *HTTP's*). Then connect to the instance using *SSH* client using your key, then enter the following command in a proper way.<br>

> ``` ssh -i "airflow_ec2_key.pem" os@ec2-id.region.compute.amazonaws.com ```  <br>

Then run the following commands: (ubuntu case) <br>

> ```sudo apt-get update``` <br>
> ```sudo apt install python-pip ``` <br>
> ```sudo pip install apache-airflow ``` <br>
> ```sudo pip install s3fs ``` <br>
> ```sudo pip install pandas``` <br>

Followed by: <br>

> ```airflow standalone``` <br>


Then be sure to get your *user* and your *password*. Now you could go to the public dns (be sure to check in-bound rules), then use the former keys to acces to the *Airflow Dashboard*.

Now we create the *DAG* file. Remember that this benefits from **Directed Acyclic Graphs** because this induces a *partial ordering* betweeen our tasks and this is used to properly improve *scheduling* for systems, in this case, Airflow.

In this project, our *DAG* file will contain the *default_arguments* mentioned previusly, after that we will only create the DAG tasks (one as a 1 time event and the other as an scheduled event). 

Of course you will need a location t storage the final *csv* file, in order to do that you have to go to *s3* in **AWS** an create a bucket. (You should use the same region as the *ec2* instance).
Then, the last line of *twitter_etl.py* should actually look like: <br>

> ``` df.to_csv('s3://unique-bucket-name/refined_tweets.csv')``` <br>

Then we are ready to deploy the DAG. Simply go to the **SSH** connection and go to the *airflow* folder in your *ec-2* instance, create a *DAG* location (this is where the two **py** scripts belong) and go to the *airflow.cfg* file and edit the default *DAG* location, then go to the *DAG* folder and type: <br>

> ``` sudo nano twitter_dag.py``` <br>

And copy the pertinent content. 
(Also you could do this manually in the Airflow dashboard that you are currently hosting)

Then using the *dashboard* you can click on the *twitter_dag.py*, go to graph and then click on *run*. (Be sure to have all the needed permitions in our services). Once it is done you can go to your bucket and have your data ready to do all the fancy analysis.


### *Done by jdpalmad*
