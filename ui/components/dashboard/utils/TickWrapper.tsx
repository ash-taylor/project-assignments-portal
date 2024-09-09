import React from 'react';

interface CustomTickProps {
  x?: number;
  y?: number;
  payload?: {
    value: any;
  };
}

const CustomXAxisTick: React.FC<CustomTickProps> = ({ x, y, payload }) => {
  if (x === undefined || y === undefined || !payload) {
    return null;
  }

  return (
    <g transform={`translate(${x},${y})`}>
      <text
        x={0}
        y={0}
        dy={20}
        textAnchor="end"
        fill="#666"
        transform="rotate(-35)"
      >
        {payload &&
        payload.value &&
        typeof payload.value === 'string' &&
        payload.value.length > 10
          ? `${payload.value.substring(0, 10)}...`
          : payload.value}
      </text>
    </g>
  );
};

const CustomXAxisTickWrapper = (props: CustomTickProps) => (
  <CustomXAxisTick {...props} />
);

export default CustomXAxisTickWrapper;
