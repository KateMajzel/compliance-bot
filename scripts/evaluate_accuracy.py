import json
import os
from pii_detector import PIIDetector

class PIIEvaluator:
    def __init__(self):
        self.detector = PIIDetector()
    
    def create_ground_truth(self):
        """
        Co POWINNO być wykryte
        """
        ground_truth = {
            'document1.txt': {
                'expected_pii': [
                    {'type': 'Imię i nazwisko', 'value': 'Jan Kowalski'},
                    {'type': 'PESEL', 'value': '90010112345'},
                    {'type': 'Telefon', 'value': '+48 123 456 789'},
                    {'type': 'Email', 'value': 'jan.kowalski@example.com'},
                    {'type': 'Adres', 'value': 'ul. Kwiatowa 15/3, 00-001 Warszawa'},
                    {'type': 'Numer konta', 'value': '12 3456 7890 1234 5678 9012 3456'}
                ],
                'expected_count': 6,
                'expected_risk': 'high'
            },
            'document2.txt': {
                'expected_pii': [
                    {'type': 'Imię i nazwisko', 'value': 'Anna Nowak'},
                    {'type': 'PESEL', 'value': '85020298765'},
                    {'type': 'NIP', 'value': '1234567890'},
                    {'type': 'Telefon', 'value': '600 700 800'},
                    {'type': 'Email', 'value': 'anna.nowak@email.pl'},
                    {'type': 'Adres', 'value': 'ul. Polna 8, 30-001 Kraków'},
                    {'type': 'Numer konta', 'value': '98 7654 3210 9876 5432 1098 7654'}
                ],
                'expected_count': 7,
                'expected_risk': 'high'
            },
            'document3.txt': {
                'expected_pii': [],
                'expected_count': 0,
                'expected_risk': 'low'
            },
            'document4.txt': {
                'expected_pii': [
                    {'type': 'Imię i nazwisko', 'value': 'Piotr Wiśniewski'},
                    {'type': 'PESEL', 'value': '88030312345'},
                    {'type': 'Imię i nazwisko', 'value': 'Maria Zielińska'},
                    {'type': 'PESEL', 'value': '92051298765'},
                    {'type': 'Imię i nazwisko', 'value': 'Tomasz Kamiński'},
                    {'type': 'PESEL', 'value': '79120567890'}
                ],
                'expected_count': 6,
                'expected_risk': 'high'
            }
        }
        
        # Zapisz ground truth
        with open('results/ground_truth.json', 'w', encoding='utf-8') as f:
            json.dump(ground_truth, f, ensure_ascii=False, indent=2)
        
        return ground_truth
    
    def calculate_metrics(self, detected, expected):
        """
        Oblicza metryki: Precision, Recall, F1-Score
        """
        detected_values = set([item['value'] for item in detected])
        expected_values = set([item['value'] for item in expected])
        
        true_positives = len(detected_values.intersection(expected_values))
        false_positives = len(detected_values - expected_values)
        false_negatives = len(expected_values - detected_values)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1_score, 3)
        }
    
    def evaluate_all(self):
        """
        Ewaluacja wszystkich dokumentów
        """
        print("\n" + "="*70)
        print("📊 EWALUACJA DOKŁADNOŚCI WYKRYWANIA PII")
        print("="*70 + "\n")
        
        ground_truth = self.create_ground_truth()
        
        documents = [
            'documents/document1.txt',
            'documents/document2.txt',
            'documents/document3.txt',
        ]
        
        all_metrics = []
        
        for doc_path in documents:
            if not os.path.exists(doc_path):
                continue
            
            doc_name = os.path.basename(doc_path)
            print(f"\n📄 Dokument: {doc_name}")
            print("-" * 70)
            
            # Analiza dokumentu
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = self.detector.detect_pii_with_ai(content)
            
            if not result:
                print("❌ Błąd podczas analizy")
                continue
            
            # Porównanie z ground truth
            gt = ground_truth[doc_name]
            metrics = self.calculate_metrics(
                result['pii_items'],
                gt['expected_pii']
            )
            
            # Wyświetlenie wyników
            print(f"Wykryte PII: {len(result['pii_items'])} / Oczekiwane: {gt['expected_count']}")
            print(f"\nMetryki:")
            print(f"  ✓ True Positives:  {metrics['true_positives']}")
            print(f"  ✗ False Positives: {metrics['false_positives']}")
            print(f"  ✗ False Negatives: {metrics['false_negatives']}")
            print(f"\n  📈 Precision: {metrics['precision']:.1%}")
            print(f"  📈 Recall:    {metrics['recall']:.1%}")
            print(f"  📈 F1-Score:  {metrics['f1_score']:.1%}")
            
            all_metrics.append({
                'document': doc_name,
                'metrics': metrics,
                'detected_count': len(result['pii_items']),
                'expected_count': gt['expected_count']
            })
        
        # Średnie metryki
        avg_precision = sum(m['metrics']['precision'] for m in all_metrics) / len(all_metrics)
        avg_recall = sum(m['metrics']['recall'] for m in all_metrics) / len(all_metrics)
        avg_f1 = sum(m['metrics']['f1_score'] for m in all_metrics) / len(all_metrics)
        
        print("\n" + "="*70)
        print("📊 ŚREDNIE METRYKI")
        print("="*70)
        print(f"Precision: {avg_precision:.1%}")
        print(f"Recall:    {avg_recall:.1%}")
        print(f"F1-Score:  {avg_f1:.1%}")
        
        # Zapis raportu
        evaluation_report = {
            'individual_results': all_metrics,
            'average_metrics': {
                'precision': round(avg_precision, 3),
                'recall': round(avg_recall, 3),
                'f1_score': round(avg_f1, 3)
            }
        }
        
        with open('results/evaluation_report.json', 'w', encoding='utf-8') as f:
            json.dump(evaluation_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Raport zapisany: results/evaluation_report.json\n")

if __name__ == "__main__":
    evaluator = PIIEvaluator()
    evaluator.evaluate_all()