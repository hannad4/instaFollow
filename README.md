# InstaFollow - A follower tracker for Instagram

Are you a socially anxious person? 

Do you often times find yourself fearing your *meaningless friendship status* with others online? 

Have you ever wished you could track if the people you follow on sites like Instagram are people *who actually follow you back?*

**Well, look no further!**

InstaFollow is a python built bot that will do the hard work for you. Just type in your username and password, and watch the magic happen!<br><br>

# Current Status
**<ul>This project is considered completed by myself (the developer) at this time, and is ready for use. Before using, please carefully read the instructions and FAQs below</ul>**<br>


# Downloading the Program
The program can be downloaded at the releases page of this repository. Just download the `.exe` file.<br><br>

# Running the Program
To run & use the program, follow these simple steps:

 1. Open/run the file you downloaded

 2. Follow the instructions that are prompted to you
    
    *GREEN prompts are simple information dialog prompts shown to you so that you may understand what the program is doing. PINK prompts are prompts which require your intervention or input*
 
 3. Wait for the output to be resulted. The time this will take to complete will vary depending on how many followers you have and how many people you follow<br><br>

 # FAQs
<h3><b>1. There's a million other programs like this out in the wild. Why should I use this one?</b></h3>
<br>While the internet is filled to the brim with applications like these, many of these programs will require extraneous amounts of effort from the user. These actions will include things such as manually searching for an instagram user ID (which is different from the username), requiring manual compilation of the program, & requiring arguments to be included when running the program. Most users will find these necessities to be a hassle. <br><br>
This program aims to keep it simple. Just download one program that runs via your machine's built in terminal, follow the two primary input prompts, and enjoy the results.<br><br>
<h3><b>2. How can I be sure this program is not malicious?</b><br></h3>
<br>Your personal information is highly sensitive, and it is treated as such. For example, when prompting for your password, Python's <code>getpass()</code> module is utilized for echoless output. The data you enter is sent to one place only - Instagram's login form. <br><br>
Additionally, upon termination of the program, a garbage collector is manually invoked to clean all system memory utilized by the program, eliminating residual data from remaining on your machine post-program completion. <br><br>
Best of all, this program is open source! You can see the exact code that was used to compile the executable program on this GitHub Repo, & can even download it and modify/compile it to your heart's content, until you are satisfied. 
<br><br>
<h3><b>3. When attempting to run this program, my system notified me that it blocked a Trojan Virus. Why did this happen?</b><br></h3><br>
An antivirus program "detects" a virus in several ways, including analyzing a program's behavior and certificate signing. Since instaFollow is an unsigned program that automates a web browser, it will not be surprising for it to be detected as a "virus."
<br><br>
Additionally, <code>PyInstaller</code> is a python package that was utilized to freeze this program into the current release files. Executable files that are generated via PyInstaller will commonly be picked up by anti-virus programs as a false positive. 
<br><br>
If the program gets blocked on your machine, simply "allow the threat" in your antivirus program. This means you are telling your anti-virus that the program you are trying to run is not malicious & can be run. 
<br><br>
<h3><b>4. My macine's firewall is asking me if I want to allow network access for this program?</b><br></h3>
<br>
This access should not be required for the program to run successfully. When your machine detects a program is attempting a network connection, your firewall will prompt to ask if this program should be allowed to "talk" to the outside world, & whether it should do so on public or private networks. However, regardless of which access you allow, the program should still be able to grab the Instagram page & function as normally.
<br><br>
<h3><b>5. Every time I use the program, Instagram emails me saying a new log in has occurred? </b><br></h3>
<br>
This program uses a special version of Chrome called the <code>ChromeWebDriver</code>. Every time the program is run, a new instance of this verison of Chrome is iniated and used. When the program completes, all of this browser's cookies are deleted, and the program's memory is cleared. As a result, when an Instagram login occurs using this verison of Chrome, Instagram will not find any other ChromeWebDriver sessions matching to each other. 
<br><br>
In other words, every login that occurs is completely unique from its predecessors & from any future log ins. This is why Instagram sends you the "new login" email. Instagram will automatically remove the other browser sessions from their database after some time, to ensure security.  
<br><br>

<h3><b>6. The program looks like it is loading something but it is taking forever, what's going on? </b><br></h3>
<br>
This program is built using only Python modules & libraries, and avoids using the Instagram API. As a result, one of the things the program must do is manually load your followers & following lists. Due to limitations of the web version of Instagram, only 12 names can be loaded at a time. As a result, the program must record the 12 names, and then manually scroll until through the list until it reaches the end. As a result, the more users you have following your (or the more users you are following), the longer it will take for the program to gather the whole list. 
<br><br>
But the beauty of this program is that you can just chill out while it does the annoying work for you! Just leave it open in the background & check on it later. 
