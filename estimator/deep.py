import tensorflow as tf
from tensorflow.contrib.layers import fully_connected

RELU_E = 0.001
DROPOUT = 0.5
MOMENTUM = 0.5


def deep_q_estimator(X, y, move_mask, output_count, lr, epsilon=RELU_E, dropout=DROPOUT, momentum=MOMENTUM):

    layer_1 = fully_connected(X, num_outputs=128)
    dropout_1 = tf.nn.dropout(layer_1, dropout, name='dropout_1')
    variable_summaries(dropout_1)

    layer_2 = fully_connected(dropout_1, num_outputs=256)
    dropout_2 = tf.nn.dropout(layer_2, dropout, name='dropout_2')
    variable_summaries(dropout_2)

    layer_3 = fully_connected(dropout_2, num_outputs=520)
    dropout_3 = tf.nn.dropout(layer_3, dropout, name='dropout_3')
    variable_summaries(dropout_3)

    layer_4 = fully_connected(dropout_3, num_outputs=256)
    dropout_4 = tf.nn.dropout(layer_4, dropout, name='dropout_4')
    variable_summaries(dropout_4)

    layer_5 = fully_connected(dropout_4, num_outputs=96)
    dropout_5 = tf.nn.dropout(layer_5, dropout, name='dropout_5')
    variable_summaries(dropout_5)

    output = fully_connected(dropout_5, num_outputs=output_count)
    variable_summaries(output)

    loss = tf.reduce_sum(move_mask * tf.square(y - output))
    optimizer = tf.train.RMSPropOptimizer(lr, momentum=momentum)
    train = optimizer.minimize(loss)

    tf.summary.scalar('loss', loss)
    summaries = tf.summary.merge_all()

    return output, train, summaries


def variable_summaries(var):
    """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))

        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)
