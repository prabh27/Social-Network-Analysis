/*-------------------------------------------      Prabh Simran Singh Baweja
 
                                                        IIIT Hyderabad -------------------------------------------------------------------*/

#include <bits/stdc++.h>

#define mod 1000000007
#define ll long long
#define clr(a) memset(a,0,sizeof(a))

using namespace std;

int main()
{
    fstream myfile;
    ofstream myfile2;
    myfile.open("file2.txt");                  // Opens the file containing all the comments and the commentors, commented_on info. 
    string line;
    map<string, map<string, int> > users;      // Contains all the users. 
    if(myfile.is_open())
    {
        string preuser = "";
        string preuser2 = "";
        while(getline(myfile, line))
        {
            string user = "";
            int temp = 0;
            string main = "";
            string comment = "";
            string main2 = "";
            int i = 0;
            while(i < line.size())
            {
                if(temp == 0 && line[i] == '@' && line[i+1] == 'N') // Extracting commentor_id.
                {
                    temp = 1;
                    user += line[i];
                    user += line[i+1];
                    user += line[i+2];
                    user += line[i+3];
                    i = i+4;
                    user.erase(remove_if(user.begin(), user.end(), ::isspace),user.end());
                    if(users.find(user) == users.end())
                    {
                        map<string, int> a;
                        users[user] = a;
                    }
                    temp = 2;
                    main = user;
                    preuser = main;
                //    cout<<"USER "<<user<<endl;
                    user = "";
                    while(line[i] != '@' && line[i+1] != 'N')   // Extracting commented_on id
                    {
                        user+=line[i];
                        i++;
                    }
                    if(line[i] == '@' && line[i+1] == 'N')
                    {
                        user += line[i];
                        user += line[i+1];
                        user += line[i+2];
                        user += line[i+3];
                        i = i+4;
                    }
                    user.erase(remove_if(user.begin(), user.end(), ::isspace),user.end()); // Remove extra white spaces.
                    map<string, int> m;
                    m = users[main];
                    if(m.find(user) == m.end())
                    {
                        m[user] = 1;
                    }
                    else
                        m[user]++;
                    main2 = user;
                    preuser2 = main2;
                    //cout<<"USER2 "<<main2<<endl;
                    user = "";
                    comment = "";
                }
                user += line[i];
                comment += line[i];                // Extracting the comments.
                i++;
            }
            //cout<<"Comment "<<comment<<endl;
            if(main == "")
            {
                map<string, int> my;
                my = users[preuser];
                my[preuser2]++;
            }
            myfile2.open(main.c_str(),std::ios_base::app);      // Opening the file commentor_id.
            myfile2<<main2<<" ";                                // Adding commented_on id.
            myfile2<<comment<<endl;                              // Adding comments. 
            myfile2.close();
        }
    }
	return 0;
}

