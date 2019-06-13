import tensorflow as tf
import numpy as np
from card_game import *



num_inputs = 2 * 16
num_hidden = int(2 * num_inputs * 1.5)
num_outputs = 23

initializer = tf.contrib.layers.variance_scaling_initializer()

X = tf.placeholder(tf.float32, shape = [None, num_inputs])

hidden_layer_one = tf.layers.dense(X, num_hidden,activation=tf.nn.relu,
	kernel_initializer=initializer)

hidden_layer_two = tf.layers.dense(hidden_layer_one,num_hidden,activation=tf.nn.relu,
	kernel_initializer=initializer)

hidden_layer_three = tf.layers.dense(hidden_layer_two,num_hidden,activation=tf.nn.relu,
	kernel_initializer=initializer)

output_layer = tf.layers.dense(hidden_layer_three, num_outputs,activation=tf.nn.sigmoid,
	kernel_initializer=initializer)

probabilities = tf.concat(axis=1,values=[output_layer])
action = tf.multinomial(probabilities,num_samples=1)

init = tf.global_variables_initializer()

epi = 50000
step_limit = 500
#env = game()
avg_steps = []
rewards = []

with tf.Session() as sess:
	init.run()

	for i_episode in range(epi):
		obs = reset()

		for s in range(step_limit):
			action_val = action.eval(feed_dict = {X:obs.reshape(1,num_inputs)})
			obs,reward,done = step(action_val[0][0])

			if done:
				print("Reward: " + str(reward))
				rewards.append(reward)
				avg_steps.append(s)
				#print("Done after {} steps.".format(s))
				print("The sum of your rewards is {}".format(sum(rewards)))
				break

print(sum(rewards))





#tf stuff
'''
observations = tf.placeholder(tf.int32, shape=(14,2))
#maybe make int?

actions = tf.placeholder(tf.float32, shape = [None])

#model
Y = tf.layers.dense(observations, 200, activation=tf.nn.relu)
Ylogits = tf.layers.dense(Y,13)

#sample an action from predicted probabilities
sample_op = tf.multinomial(logits = Ylogits, num_samples=1)

#loss
cross_entropies = tf.losses.softmax_cross_entropy(onehot_labels=
	tf.one_hot(actions,13), logits = Ylogits)

loss = tf.reduce_sum(rewards * cross_entropies)

#training operation
optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001, decay=.99)
train_op = optimizer.minimize(loss)

with tf.Session as sess:
	...
	observation = return_observation(playerList[0])
	while not done: 
		action = sess.run(sample_op, feed_dict = {observations: [observation]})
		print("HEY HEY HEY")
		reward = cardGame.step(action)
		observations.append(observation)
		actions.append(action)
		rewards.append(reward)
'''