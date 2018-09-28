def training(x_name,y_name,model=final_model):
    x_train = np.load('./x_train/'+x_name)
    y_train = np.load('./y_train/'+y_name)
	
	y_oh_list=list()

    for trend in y_train:
		new_value=value+1
		code = [0 for _ in range(3)]
		code[new_value]=1
		y_oh_list.append(code)
	y_train_end=np.asarray(y_oh_list)
    #encoder = LabelEncoder()
    #encoder.fit(y_train)
    #encoded_Y = encoder.transform(y_train)
    #y_train_end = to_categorical(encoded_Y)
    print("model fitting on "+x_name)
    
    final_model.fit(x_train, y_train_end, validation_split=0.2,epochs=1)
