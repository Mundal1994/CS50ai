# cs50ai-traffic

EXPERIMENTATION PROCESS OF MAKING THE GET_MODEL

I started out by doing my own research to get a better unstanding of how to use the tensorflow library's functions. I tried a bunch of different things but the below result was the result from the first model I made (it consisted of a lot of layers with anything from 42 - 84 filters)

        loss: 0.6931 - accuracy: 0.0059 - 1s/epoch - 3ms/step

I had a lot of trouble in the beginning making the model. I usually do a lot of trying out and based on my failures and succeeses I learn but with this particular assignment that approach didn't work out that well. So I might have realized rather late that I had to go back to researching.

While on google I stumbled upon this article: https://medium.com/@sdoshi579/convolutional-neural-network-learn-and-apply-3dac9acfe2b6. It helped me understand the 'Convolutional Neural Network' a lot more. I tried to run their implementation as a comparison with the testcase we have gotten for this module in the hopes of understanding it better. The accuracy was very good around 0.97 but the downside on theirs was that because they had a lot of layers, dense layers, dropouts etc... it was very slow to run through all of the testcases. It had an average on 30 sec per iteration. I did try to move stuff around / delete functions in their implementation to see how that affected the overall result.

After this article I started over with a greater understanding of 'Convolutional Neural Network' and how they should be implemented. I wanted to keep it simple while also making sure it wasn't too slow. So I tried this time to keep it at 2 layers with a filter of 16 and 32. After each of those I decided to run the BatchNormalization to normalize contributions to a layer, MaxPooling2D to downsample the input and Dropout to prevent overfitting on the training data.

I also tried to run my implementation without BatchNormalization and Maxpooling2D present and having those functions didn't affect the accuracy as much as I thought but since I didn't know how accurate we had to make the model I decided to keep them in as they did make it a bit better accuracy (the speed was also not greatly affected by keeping those functions in).


CONCLUSION

I noticed that more layers doesn't always mean that the model will become better and a lot of times a simpler model can make for a better result. At least the model I ended up with was a lot simpler than what I started out with. 
