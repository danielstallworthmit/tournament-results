Swiss-PairingTournament Results

Description:
	Stores the results of a Swiss-Pairing tournament in a postgresql database. Tournament.py creates players and matches, and determines who should be matched next based on their rank in the tournament database. Test functions make sure the matching is determined properly.

Prerequisites:
 - 	Install Vagrant and VirtualBox
 - 	Clone the fullstack-nanodegree-vm repository
 - 	Launch the Vagrant VM in terminal using ‘vagrant up’ and ‘vagrant ssh’
 - 	Replace files in /vagrant/tournament folder with the files listed below:
 		tournament.sql: Database schema to create the tables and views used
		tournament.py: Tournament logic 
		tournament_test.py: Test functions to test the logic in tournament.py
 -	Create the tournament database and the tables from tournament.sql in the VM:
		vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql 
		vagrant=> \i tournament.sql 
		vagrant=> \q 
 
Run the test functions to make sure everything passes:
	vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py

You should see the following output if successful:
	1. Old matches can be deleted. 	2. Player records can be deleted. 	3. After deleting, countPlayers() returns zero. 	4. After registering a player, countPlayers() returns 1. 	5. Players can be registered and deleted. 	6. Newly registered players appear in the standings with no matches. 	7. After a match, players have updated standings. 	8. After one match, players with one win are paired. 	Success! All tests pass!





