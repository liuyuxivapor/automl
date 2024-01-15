import re
import matplotlib.pyplot as plt

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def extract_info(log_lines):
    model_info = []
    current_model = {"FC1": None, "FC2": None, "FC3": None, "accuracy": None, "size": None}
    
    for line in log_lines:
        match_params = re.match(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2} [APMapm]{2}) \| Parameters:", line)
        match_fc1 = re.match(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2} [APMapm]{2}) \| FC1=(\d+)", line)
        match_fc2 = re.match(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2} [APMapm]{2}) \| FC2=(\d+)", line)
        match_fc3 = re.match(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2} [APMapm]{2}) \| FC3=(\d+)", line)
        match_size = re.match(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2} [APMapm]{2}) \| model size: (\d+\.\d+) KB", line)
        match_accuracy = re.match(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2} [APMapm]{2}) \| Final best Prec = (\d+\.\d+)%", line)
        
        if match_params:
            current_model = {"FC1": None, "FC2": None, "FC3": None, "accuracy": None, "size": None}
        elif match_fc1:
            current_model["FC1"] = int(match_fc1.group(2))
        elif match_fc2:
            current_model["FC2"] = int(match_fc2.group(2))
        elif match_fc3:
            current_model["FC3"] = int(match_fc3.group(2))
        elif match_size:
            current_model["size"] = float(match_size.group(2))
        elif match_accuracy:
            current_model["accuracy"] = float(match_accuracy.group(2)) / 100  # Convert percentage to decimal
            model_info.append(current_model)
    
    return model_info

def calculate_combined_metric(accuracy, size_normalized, weight):
    return weight * accuracy + (1 - weight) * (1 - size_normalized)

def choose_best_model(models, weight):
    best_model = None
    best_metric = float('-inf')

    for model in models:
        combined_metric = calculate_combined_metric(model["accuracy"], model["size"], weight)
        # print(model["accuracy"], model["size"], weight)
        if combined_metric > best_metric:
            best_metric = combined_metric
            best_model = model

    return best_model

def plot_scatter(models, weight):
    accuracies = [model["accuracy"] for model in models]
    sizes = [model["size"] for model in models]
    combined_metrics = [calculate_combined_metric(model["accuracy"], model["size"], weight) for model in models]

    plt.scatter(sizes, accuracies, c=combined_metrics, cmap='viridis', alpha=0.7, edgecolors="k", linewidth=0.5)
    plt.xlabel('Model Size (KB)')
    plt.ylabel('Accuracy')
    plt.title('Model Evaluation')
    plt.colorbar(label='Combined Metric')
    plt.show()

    
log_file_path = "/home/vapor/code/automl/log/dct/automl_nn_ax_2.log"
log_lines = read_log_file(log_file_path)
models = extract_info(log_lines)

weight = 0.9

best_model = choose_best_model(models, weight)

if best_model:
    print(f"The best model is:")
    print(f"FC1-FC2-FC3: {best_model['FC1'], best_model['FC2'], best_model['FC3']}")
    print(f"Accuracy: {best_model['accuracy']}")
    print(f"Size: {best_model['size']} KB")
    plot_scatter(models, weight)
