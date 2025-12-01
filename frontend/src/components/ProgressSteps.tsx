import React from 'react';
import { Upload, FileText, CreditCard, Download, Check } from 'lucide-react';

interface ProgressStepsProps {
  currentStep: 1 | 2 | 3 | 4;
}

const steps = [
  { number: 1, label: 'Upload', icon: Upload },
  { number: 2, label: 'Processamento', icon: FileText },
  { number: 3, label: 'Pagamento', icon: CreditCard },
  { number: 4, label: 'Download', icon: Download },
];

const ProgressSteps: React.FC<ProgressStepsProps> = ({ currentStep }) => {
  return (
    <div className="progress-container">
      <div className="progress-steps">
        {steps.map((step) => {
          const Icon = step.icon;
          const isCompleted = currentStep > step.number;
          const isActive = currentStep === step.number;

          return (
            <div
              key={step.number}
              className={`progress-step ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
            >
              <div className="progress-step-icon">
                {isCompleted ? <Check size={20} /> : <Icon size={20} />}
              </div>
              <span>{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProgressSteps;
