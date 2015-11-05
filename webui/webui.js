var headServerUrl = "http://192.168.140.16:5000";

if(Meteor.isClient) {

	Session.setDefault('leftEye', 50);
	Session.setDefault('rightEye', 50);
	Session.setDefault('craziness', 10);


	Template.bodyPartStatus.helpers({
		leftEye: function () {
			return Session.get('leftEye');
		},
		rightEye: function () {
			return Session.get('rightEye');
		}
	});

	Template.turnButton.events({
		'click .turn': function (event) {
			var turnRate = 10;
			var parts = $(event.target).attr('id').split('-');
			var bodyPart = parts[0];
			var sessionName = bodyPart;
			var direction = parts[1];

			var previousState;
			if (bodyPart == 'bothEyes') {
				// Use left eye when moving both eyes
				sessionName = 'leftEye';
			}

			previousState = Session.get(sessionName);
			var newState = 50;

			if (direction == 'right') {
				newState = previousState + turnRate;
			} else {
				newState = previousState - turnRate;
			}
			Meteor.call('moveBodyPart', bodyPart, previousState, newState);
			
			if (bodyPart == 'bothEyes') {
				Session.set('leftEye', newState);
				Session.set('rightEye', newState);
			} else {
				Session.set(sessionName, newState);
			}
		}
	});

	Template.brows.events({
		'click #wink': function() {
			Meteor.call('moveBodyPart', "right-brow,left-brow", 0, 60);
		},
		'click #neutral': function() {
			Meteor.call('turnBodyPart', "left-brow", 50);
			Meteor.call('turnBodyPart', "right-brow", 50);
		},
		'click #angry': function() {
			Meteor.call('turnBodyPart', "left-brow", 100);
			Meteor.call('turnBodyPart', "right-brow", 0);
		},
		'click #mellow': function() {
			Meteor.call('turnBodyPart', "left-brow", 0);
			Meteor.call('turnBodyPart', "right-brow", 100);
		}
	});
	
	Template.panicButton.events({
		'click #goCrazy': function() {
			var insanityFactor = $('#insanityFactor').val();
			Session.set('craziness', insanityFactor);
			Meteor.call('goCrazy', insanityFactor);
		}
	});
	
	Template.panicButton.helpers({
		craziness: function () {
			return Session.get('craziness');
		}
	});

	Template.commandButton.events({
		'click': function() {
			var commands = $(event.target).data('call').split("::");
			for (var i in commands) {
				Meteor.call('runAnyCommand', commands[i]);
				
				var splitted = commands[i].split('/');
				if (splitted[0] == 'turn') {
					if (splitted[1] == 'left-eye') {
						Session.set('leftEye', splitted[2]);
					}
					if (splitted[1] == 'right-eye') {
						Session.set('rightEye', splitted[2]);
					}
				}
			}
		}
	});
}

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});

	Meteor.methods({
		moveBodyPart: function(bodyPart, previousState, newState) {

			var mapping = {
				leftEye: 'left-eye',
				rightEye: 'right-eye',
				bothEyes: 'left-eye,right-eye'
			}

			var command = bodyPart;
			if (typeof mapping[bodyPart] !== 'undefined') {
				command = mapping[bodyPart];
			}

			var headCall = [
				headServerUrl,
				"multimove",
				command,
				previousState,
				newState,
				1
			].join('/');

			console.log(headCall);

			try {
				var result = HTTP.call("GET", headCall, {});
			} catch (e) {
				console.log(e);
				return false;
			}
		},
		turnBodyPart: function(bodyPart, angle) {
			var headCall = [
				headServerUrl,
				"turn",
				bodyPart,
				angle
			].join('/');

			console.log(headCall)

			try {
				var result = HTTP.call("GET", headCall, {});
			} catch (e) {
				console.log(e);
				return false;
			}
		},
		goCrazy: function(insanityFactor) {
			var message = [headServerUrl, 'crazy', insanityFactor].join('/');
			console.log(message);
			HTTP.call("GET", message)
		},
		runAnyCommand: function(command) {
			var message = [headServerUrl, command].join('/');
			console.log(message);
			HTTP.call("GET", message);
		}
	});
}

