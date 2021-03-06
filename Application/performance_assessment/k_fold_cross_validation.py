from data_extraction.convert_numpy.convert_numpy import ConvertNumpy
from performance_assessment.predict_output import PredictOutput
from performance_assessment.residual_sum_squares import ResidualSumSquares

class KFoldCrossValidation:
    # Usage:
    #   Computes K Fold Cross Validation

    def __init__(self):
        # Usage:
        #       Constructor for KFoldCrossValidation, used to setup ConvertNumpy class to convert pandas
        #       data to numpy.
        # Arguments:
        #       None

        # Create an instance of the Convert Numpy class
        self.convert_numpy = ConvertNumpy()

        # Create an instance of the Predict Output Class
        self.predict_output = PredictOutput()

        # Create an instance of the Residual Sum Squares Class
        self.residual_sum_squares = ResidualSumSquares()

    def k_fold_cross_validation(self, k, data, model, model_parameters, output, features):
        # Usage:
        #       Takes in our data, and splits the data to smaller subsets, and these smaller subsets
        #       are used as validation sets, and everything else not included in the validation set is used
        #       as training sets. The model will be trained using the training set, and the performance assessment
        #       such as RSS would be used on the validation set against the model.
        # Parameters:
        #       k                (int)            : number of folds
        #       data             (pandas object)  : data used for k folds cross validation
        #       model            (object)         : model used for k folds cross validation
        #       model_parameters (dict)           : model parameters to train the specified model
        #       features         (list of string) : a list of feature names
        #       output           (string)         : output name
        # Return:
        #       validation_error (double)        : average validation error

        # Get the length of the data
        length_data = len(data)

        # Sum of the validation error, will divide by k (fold) later
        validation_error_sum = 0

        # Loop through each fold
        for i in range(k):

            # Compute the start section of the current fold
            start = int((length_data*i)/k)

            # Compute the end section of the current fold
            end = int((length_data*(i+1))/k-1)

            # Get our validation set from the start to the end+1 (+1 since we need to include the end)
            # <Start : end + 1> Validation Set
            validation_set = data[start:end+1]

            # The Training set the left and the right parts of the validation set
            # < 0       : Start >   Train Set 1
            # < Start   : End + 1 > Validation Set
            # < End + 1 : n >       Train Set 2
            # Train Set 1 + Train Set 2 = All data excluding validation set
            training_set = data[0:start].append(data[end+1:length_data])

            # Convert our pandas frame to numpy
            validation_feature_matrix, validation_output = self.convert_numpy.convert_to_numpy(validation_set, features,
                                                                                               output, 1)

            # Convert our pandas frame to numpy
            training_feature_matrix, training_output = self.convert_numpy.convert_to_numpy(training_set, features,
                                                                                           output, 1)

            # Create a model with Train Set 1 + Train Set 2
            final_weights = model(**model_parameters, feature_matrix=training_feature_matrix, output=training_output)

            # Predict the output of test features
            predicted_output = self.predict_output.predict_output_linear_regression(validation_feature_matrix,
                                                                                    final_weights)

            # compute squared error (in other words, rss)
            validation_error_sum += self.residual_sum_squares.residual_sum_squares_linear_regression(validation_output,
                                                                                                     predicted_output)

        # Return the validation_error_sum divided by fold
        return validation_error_sum/k
